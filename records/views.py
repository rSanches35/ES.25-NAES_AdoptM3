from django.views.generic.edit import CreateView, UpdateView, DeleteView
from django.views.generic.list import ListView
from django.contrib.auth.mixins import LoginRequiredMixin
from django.core.exceptions import PermissionDenied
from django.contrib.auth.views import LoginView
from django.contrib.auth import login
from django.shortcuts import render, redirect
from django.contrib import messages
from django.db import transaction

from django.urls import reverse_lazy
from .models import State, City, Address, Client, Relic, Adoption, AdoptionRelic, RelicImage
from .forms import CustomUserCreationForm, ClientEditForm, RelicCreateForm, RelicImageFormSet

class CustomLoginView(LoginView):
    template_name = 'registration/login.html'
    redirect_authenticated_user = True
    
    def get_success_url(self):
        return reverse_lazy('pages-HomePage')

class StateCreate(LoginRequiredMixin, CreateView):
    model = State
    fields = ['name', 'uf']
    template_name = 'records/form.html'
    success_url = reverse_lazy('pages-HomePage')

class StateUpdate(LoginRequiredMixin, UpdateView):
    model = State
    fields = ['name', 'uf']
    template_name = 'records/form.html'
    success_url = reverse_lazy('pages-HomePage')

class StateDelete(LoginRequiredMixin, DeleteView):
    model = State
    template_name = 'records/delete_confirm.html'
    success_url = reverse_lazy('pages-HomePage')

class StateList(ListView):
    model = State
    template_name = 'records/lists/state.html'



class CityCreate(LoginRequiredMixin, CreateView):
    model = City
    fields = ['name', 'state']
    template_name = 'records/form.html'
    success_url = reverse_lazy('pages-HomePage')

class CityUpdate(LoginRequiredMixin, UpdateView):
    model = City
    fields = ['name', 'state']
    template_name = 'records/form.html'
    success_url = reverse_lazy('pages-HomePage')

class CityDelete(LoginRequiredMixin, DeleteView):
    model = City
    template_name = 'records/delete_confirm.html'
    success_url = reverse_lazy('pages-HomePage')

class CityList(ListView):
    model = City
    template_name = 'records/lists/city.html'



class AddressCreate(LoginRequiredMixin, CreateView):
    model = Address
    fields = ['street', 'number', 'neighborhood', 'complement', 'city']
    template_name = 'records/form.html'
    success_url = reverse_lazy('pages-HomePage')

class AddressUpdate(LoginRequiredMixin, UpdateView):
    model = Address
    fields = ['street', 'number', 'neighborhood', 'complement', 'city']
    template_name = 'records/form.html'
    success_url = reverse_lazy('pages-HomePage')

class AddressDelete(LoginRequiredMixin, DeleteView):
    model = Address
    template_name = 'records/delete_confirm.html'
    success_url = reverse_lazy('pages-HomePage')

class AddressList(ListView):
    model = Address
    template_name = 'records/lists/address.html'



class ClientCreate(LoginRequiredMixin, CreateView):
    model = Client
    fields = ['user', 'name', 'nickname', 'birth_date', 'address']
    template_name = 'records/form.html'
    success_url = reverse_lazy('pages-HomePage')
    
    def form_valid(self, form):
        form.instance.created_by = self.request.user
        return super().form_valid(form)
    
    def get_form(self, form_class=None):
        form = super().get_form(form_class)
        # Filtrar apenas usuários que não têm client_profile
        from django.contrib.auth.models import User
        form.fields['user'].queryset = User.objects.filter(client_profile__isnull=True)
        return form

class ClientUpdate(LoginRequiredMixin, UpdateView):
    model = Client
    form_class = ClientEditForm
    template_name = 'records/client_edit.html'
    success_url = reverse_lazy('pages-HomePage')
    
    def get_queryset(self):
        # Superusuários podem editar todos os clientes, usuários normais apenas os seus
        if self.request.user.is_superuser:
            return Client.objects.all()
        return Client.objects.filter(created_by=self.request.user)
    
    def form_valid(self, form):
        messages.success(self.request, 'Perfil atualizado com sucesso!')
        return super().form_valid(form)

class ClientDelete(LoginRequiredMixin, DeleteView):
    model = Client
    template_name = 'records/delete_confirm.html'
    success_url = reverse_lazy('pages-HomePage')
    
    def get_queryset(self):
        # Superusuários podem excluir todos os clientes, usuários normais apenas os seus
        if self.request.user.is_superuser:
            return Client.objects.all()
        return Client.objects.filter(created_by=self.request.user)

class ClientList(LoginRequiredMixin, ListView):
    model = Client
    template_name = 'records/lists/client.html'
    
    def get_queryset(self):
        # Exibe todos os clientes do sistema, não apenas os criados pelo usuário
        return Client.objects.all().order_by('-register_date')



class RelicCreate(LoginRequiredMixin, CreateView):
    model = Relic
    form_class = RelicCreateForm
    template_name = 'records/relic_create.html'
    success_url = reverse_lazy('pages-HomePage')
    
    def get_success_url(self):
        next_url = self.request.GET.get('next')
        if next_url:
            return next_url
        return super().get_success_url()
    
    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        # Passar o parâmetro next para o template para usar no botão cancelar
        context['next_url'] = self.request.GET.get('next', reverse_lazy('pages-HomePage'))
        
        if self.request.POST:
            context['image_formset'] = RelicImageFormSet(
                self.request.POST, 
                self.request.FILES, 
                queryset=RelicImage.objects.none(),
                prefix='form'
            )
        else:
            context['image_formset'] = RelicImageFormSet(
                queryset=RelicImage.objects.none(),
                prefix='form'
            )
        return context
    
    def form_valid(self, form):
        context = self.get_context_data()
        image_formset = context['image_formset']
        
        with transaction.atomic():
            # Definir created_by e client
            form.instance.created_by = self.request.user
            
            # Automaticamente definir client como o client_profile do usuário logado
            try:
                user_client = getattr(self.request.user, 'client_profile', None)
                if not user_client:
                    # Se não encontrar, criar um cliente automaticamente para o usuário
                    user_client = Client.objects.create(
                        user=self.request.user,
                        name=self.request.user.get_full_name() or self.request.user.username,
                        nickname=self.request.user.username,
                        email=self.request.user.email,
                        birth_date='1990-01-01',
                        created_by=self.request.user
                    )
                form.instance.client = user_client
            except Exception as e:
                # Em caso de erro, tentar encontrar qualquer cliente do usuário
                user_client = Client.objects.filter(created_by=self.request.user).first()
                if user_client:
                    form.instance.client = user_client
            
            # Verificar se o formset é válido primeiro
            if not image_formset.is_valid():
                return self.form_invalid(form)
            
            # Contar imagens válidas diretamente dos arquivos enviados
            image_files = [f for key, f in self.request.FILES.items() if 'image' in key and f]
            
            if not image_files:
                form.add_error(None, "É obrigatório enviar pelo menos uma imagem da relíquia.")
                return self.form_invalid(form)
            
            # Salvar a relíquia
            response = super().form_valid(form)
            
            # Processar as imagens
            image_formset.instance = self.object
            images = image_formset.save(commit=False)
            
            for i, image in enumerate(images):
                image.relic = self.object
                image.created_by = self.request.user
                image.save()
            
            # Se nenhuma imagem foi marcada como principal, marcar a primeira
            if images and not any(img.is_main for img in images):
                images[0].is_main = True
                images[0].save()
            elif len([img for img in images if img.is_main]) > 1:
                # Garantir que apenas uma imagem seja principal
                main_images = [img for img in images if img.is_main]
                for i, img in enumerate(main_images):
                    if i > 0:
                        img.is_main = False
                        img.save()
            
            messages.success(self.request, 'Relíquia criada com sucesso!')
            return response

class RelicUpdate(LoginRequiredMixin, UpdateView):
    model = Relic
    form_class = RelicCreateForm
    template_name = 'records/relic_edit.html'
    success_url = reverse_lazy('pages-HomePage')
    
    def get_success_url(self):
        next_url = self.request.GET.get('next')
        if next_url:
            return next_url
        return super().get_success_url()
    
    def get_queryset(self):
        # Superusuários podem editar todas as relíquias, usuários normais apenas as suas
        if self.request.user.is_superuser:
            return Relic.objects.all()
        return Relic.objects.filter(created_by=self.request.user)
    
    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        # Passar o parâmetro next para o template para usar no botão cancelar
        context['next_url'] = self.request.GET.get('next', reverse_lazy('pages-HomePage'))
        
        if self.request.POST:
            context['image_formset'] = RelicImageFormSet(
                self.request.POST, 
                self.request.FILES,
                queryset=self.object.images.all()
            )
        else:
            context['image_formset'] = RelicImageFormSet(queryset=self.object.images.all())
        context['existing_images'] = self.object.images.all()
        return context
    
    def form_valid(self, form):
        context = self.get_context_data()
        image_formset = context['image_formset']
        
        with transaction.atomic():
            response = super().form_valid(form)
            
            if image_formset.is_valid():
                image_formset.instance = self.object
                images = image_formset.save(commit=False)
                
                # Salvar novas imagens
                for image in images:
                    image.relic = self.object
                    image.created_by = self.request.user
                    image.save()
                
                # Deletar imagens marcadas para exclusão
                for deleted_image in image_formset.deleted_objects:
                    deleted_image.delete()
                
                # Verificar se ainda existe pelo menos uma imagem
                total_images = self.object.images.count()
                if total_images == 0:
                    form.add_error(None, "É obrigatório manter pelo menos uma imagem da relíquia.")
                    return self.form_invalid(form)
                
                # Se nenhuma imagem estiver marcada como principal, marcar a primeira
                if not self.object.images.filter(is_main=True).exists():
                    first_image = self.object.images.first()
                    if first_image:
                        first_image.is_main = True
                        first_image.save()
                
                messages.success(self.request, 'Relíquia atualizada com sucesso!')
                return response
            else:
                return self.form_invalid(form)

class RelicDelete(LoginRequiredMixin, DeleteView):
    model = Relic
    template_name = 'records/delete_confirm.html'
    success_url = reverse_lazy('pages-HomePage')
    
    def get_queryset(self):
        # Superusuários podem excluir todas as relíquias, usuários normais apenas as suas
        if self.request.user.is_superuser:
            return Relic.objects.all()
        return Relic.objects.filter(created_by=self.request.user)

class RelicList(LoginRequiredMixin, ListView):
    model = Relic
    template_name = 'records/lists/relic.html'
    
    def get_queryset(self):
        # Superusuários veem todas as relíquias, usuários normais veem apenas as suas
        if self.request.user.is_superuser:
            return Relic.objects.all().order_by('-obtained_date')
        return Relic.objects.filter(created_by=self.request.user).order_by('-obtained_date')



class AdoptionCreate(LoginRequiredMixin, CreateView):
    model = Adoption
    fields = ['relic', 'payment_status']
    template_name = 'records/form.html'
    success_url = reverse_lazy('records:AdoptionList')
    
    def form_valid(self, form):
        form.instance.created_by = self.request.user
        
        # Automaticamente definir new_owner como o client_profile do usuário logado
        try:
            user_client = getattr(self.request.user, 'client_profile', None)
            if not user_client:
                # Se não encontrar, criar um cliente automaticamente para o usuário
                user_client = Client.objects.create(
                    user=self.request.user,
                    name=self.request.user.get_full_name() or self.request.user.username,
                    nickname=self.request.user.username,
                    email=self.request.user.email,
                    birth_date='1990-01-01',
                    created_by=self.request.user
                )
            form.instance.new_owner = user_client
        except Exception as e:
            # Em caso de erro, tentar encontrar qualquer cliente do usuário
            user_client = Client.objects.filter(created_by=self.request.user).first()
            if user_client:
                form.instance.new_owner = user_client
        
        return super().form_valid(form)
    
    def get_form(self, form_class=None):
        form = super().get_form(form_class)
        # Filtrar apenas relíquias criadas pelo usuário atual
        form.fields['relic'].queryset = Relic.objects.filter(created_by=self.request.user)
        return form

class AdoptionUpdate(LoginRequiredMixin, UpdateView):
    model = Adoption
    fields = ['relic', 'payment_status']
    template_name = 'records/form.html'
    success_url = reverse_lazy('records:AdoptionList')
    
    def get_queryset(self):
        # Superusuários podem editar todas as adoções, usuários normais apenas as suas
        if self.request.user.is_superuser:
            return Adoption.objects.all()
        return Adoption.objects.filter(created_by=self.request.user)
    
    def get_form(self, form_class=None):
        form = super().get_form(form_class)
        # Superusuários veem todas as relíquias, usuários normais apenas as suas
        if self.request.user.is_superuser:
            form.fields['relic'].queryset = Relic.objects.all()
        else:
            form.fields['relic'].queryset = Relic.objects.filter(created_by=self.request.user)
        return form

class AdoptionDelete(LoginRequiredMixin, DeleteView):
    model = Adoption
    template_name = 'records/delete_confirm.html'
    success_url = reverse_lazy('records:AdoptionList')
    
    def get_queryset(self):
        # Superusuários podem excluir todas as adoções, usuários normais apenas as suas
        if self.request.user.is_superuser:
            return Adoption.objects.all()
        return Adoption.objects.filter(created_by=self.request.user)

class AdoptionList(ListView):
    model = Adoption
    template_name = 'records/lists/adoption.html'
    context_object_name = 'adoptions'
    
    def get_queryset(self):
        if self.request.user.is_authenticated:
            # Superusuários veem todas as adoções, usuários normais veem apenas as suas
            if self.request.user.is_superuser:
                return Adoption.objects.all().order_by('-created_at')
            return Adoption.objects.filter(created_by=self.request.user).order_by('-created_at')
        return Adoption.objects.none()



class AdoptionRelicCreate(LoginRequiredMixin, CreateView):
    model = AdoptionRelic
    fields = ['adoption', 'relic']
    template_name = 'records/form.html'
    success_url = reverse_lazy('records:AdoptionRelicList')
    
    def form_valid(self, form):
        form.instance.created_by = self.request.user
        return super().form_valid(form)

class AdoptionRelicUpdate(LoginRequiredMixin, UpdateView):
    model = AdoptionRelic
    fields = ['adoption', 'relic']
    template_name = 'records/form.html'
    success_url = reverse_lazy('records:AdoptionRelicList')
    
    def get_queryset(self):
        return AdoptionRelic.objects.filter(created_by=self.request.user)

class AdoptionRelicDelete(LoginRequiredMixin, DeleteView):
    model = AdoptionRelic
    template_name = 'records/delete_confirm.html'
    success_url = reverse_lazy('records:AdoptionRelicList')
    
    def get_queryset(self):
        return AdoptionRelic.objects.filter(created_by=self.request.user)

class AdoptionRelicList(ListView):
    model = AdoptionRelic
    template_name = 'records/lists/adoptionrelic.html'
    context_object_name = 'object_list'
    
    def get_queryset(self):
        if self.request.user.is_authenticated:
            return AdoptionRelic.objects.filter(created_by=self.request.user)
        return AdoptionRelic.objects.none()


class ProfileView(LoginRequiredMixin, ListView):
    model = Relic
    template_name = 'records/profile.html'
    context_object_name = 'user_relics'
    paginate_by = 6
    
    def get_queryset(self):
        return Relic.objects.filter(created_by=self.request.user).order_by('-id')
    
    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        
        # Tentar obter o perfil do cliente
        try:
            client_profile = getattr(self.request.user, 'client_profile', None)
            if not client_profile:
                # Se não encontrar, procurar por clientes criados pelo usuário
                client_profile = Client.objects.filter(created_by=self.request.user).first()
        except:
            client_profile = None
            
        context['client_profile'] = client_profile
        context['total_relics'] = self.get_queryset().count()
        context['total_adoptions'] = Adoption.objects.filter(created_by=self.request.user).count()
        
        # Adicionar adoções do usuário
        context['user_adoptions'] = Adoption.objects.filter(created_by=self.request.user).order_by('-adoption_date')
        
        return context