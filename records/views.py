from django.views.generic.edit import CreateView, UpdateView, DeleteView
from django.views.generic.list import ListView
from django.contrib.auth.mixins import LoginRequiredMixin
from django.core.exceptions import PermissionDenied
from django.contrib.auth.views import LoginView
from django.contrib.auth import login
from django.shortcuts import render, redirect
from django.contrib import messages
from django.db import transaction
from django_filters.views import FilterView
from django.core.paginator import Paginator
from django.db.models import Q, Count
from django.utils import timezone
from datetime import datetime

from django.urls import reverse_lazy
from .models import State, City, Address, Client, Relic, Adoption, AdoptionRelic, RelicImage
from .forms import CustomUserCreationForm, ClientEditForm, RelicCreateForm, RelicImageFormSet
from .filters import ClientFilter, RelicFilter

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
    paginate_by = 15  # Paginação de 15 estados por página
    
    def get_queryset(self):
        return State.objects.all().order_by('name')



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
    paginate_by = 20  # Paginação de 20 cidades por página
    
    def get_queryset(self):
        return City.objects.select_related('state').order_by('name')


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
    paginate_by = 15  # Paginação de 15 endereços por página

    def get_queryset(self):
        qs = super().get_queryset()
        return qs.select_related('city', 'city__state').order_by('street', 'number')



class ClientCreate(LoginRequiredMixin, CreateView):
    model = Client
    fields = ['user', 'name', 'nickname', 'birth_date', 'address']
    template_name = 'records/form.html'
    success_url = reverse_lazy('pages-HomePage')
    
    def form_valid(self, form):
        """Método form_valid que realiza tarefas com outras classes ao criar cliente"""
        
        with transaction.atomic():
            # 1. Configurar dados básicos
            form.instance.created_by = self.request.user
            
            # 2. Salvar o cliente
            response = super().form_valid(form)
            client = form.instance
            
            # 3. MOVIMENTO: Sincronizar dados com User se vinculado
            if client.user:
                # Atualizar email do User se necessário
                if client.user.email != client.email:
                    client.user.email = client.email
                    client.user.save()
                
                # Atualizar nome completo do User se necessário
                full_name = client.name.split(' ', 1)
                if len(full_name) >= 2:
                    client.user.first_name = full_name[0]
                    client.user.last_name = full_name[1]
                else:
                    client.user.first_name = client.name
                client.user.save()
            
            # 4. MOVIMENTO: Criar registros de auditoria/estatística
            self.create_client_activity_log(client)
            
            # 5. MOVIMENTO: Verificar e migrar relíquias órfãs
            self.assign_orphan_relics_to_client(client)
            
            # 6. Mensagem de sucesso com informações detalhadas
            relics_count = Relic.objects.filter(client=client).count()
            messages.success(
                self.request,
                f'Cliente "{client.name}" criado com sucesso! '
                f'Relíquias associadas: {relics_count}. '
                f'Usuário vinculado: {"Sim" if client.user else "Não"}'
            )
            
            return response
    
    def create_client_activity_log(self, client):
        """Método auxiliar para criar log de atividade do cliente"""
        # Atualizar last_activity
        client.last_activity = timezone.now()
        client.save()
    
    def assign_orphan_relics_to_client(self, client):
        """Método auxiliar para associar relíquias órfãs ao cliente"""
        # Se o cliente tem um User vinculado, procurar relíquias criadas por esse usuário sem cliente
        if client.user:
            orphan_relics = Relic.objects.filter(
                created_by=client.user,
                client__isnull=True
            )
            
            # Associar essas relíquias ao cliente
            for relic in orphan_relics:
                relic.client = client
                relic.save()
            
            if orphan_relics.exists():
                messages.info(
                    self.request,
                    f'{orphan_relics.count()} relíquia(s) órfã(s) foi(ram) automaticamente associada(s) ao cliente.'
                )
    
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

class ClientList(FilterView):
    model = Client
    template_name = 'records/lists/client.html'
    filterset_class = ClientFilter
    paginate_by = 10
    context_object_name = 'clients'
    
    def get_queryset(self):
        # Exibe todos os clientes do sistema com select_related para otimização
        return Client.objects.select_related('user', 'address__city__state', 'created_by').all().order_by('-register_date')
    
    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        
        # Calcular estatísticas TOTAIS do queryset completo (antes da paginação)  
        filterset = self.get_filterset(self.filterset_class)
        total_queryset = filterset.qs
        context['total_clients'] = total_queryset.count()
        
        return context



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
            relic = self.object
            
            # MOVIMENTO: Processar as imagens
            image_formset.instance = relic
            images = image_formset.save(commit=False)
            
            for i, image in enumerate(images):
                image.relic = relic
                image.created_by = self.request.user
                image.save()
            
            # Se nenhuma imagem foi marcada como principal, marcar a primeira
            if images and not any(img.is_main for img in images):
                images[0].is_main = True
                images[0].save()
            
            # MOVIMENTO: Atualizar estatísticas do cliente proprietário
            if relic.client:
                self.update_client_relic_count(relic.client)
            
            # MOVIMENTO: Criar registro automático de histórico se taxa de adoção > 0
            if relic.adoption_fee:
                self.create_adoption_availability_record(relic)
            
            # MOVIMENTO: Atualizar last_activity do cliente proprietário
            if relic.client:
                relic.client.last_activity = timezone.now()
                relic.client.save()
            
            # Mensagem de sucesso personalizada
            image_count = len(images)
            messages.success(
                self.request,
                f'Relíquia "{relic.name}" criada com sucesso! '
                f'{image_count} imagem(ns) adicionada(s). '
                f'Proprietário: {relic.client.name if relic.client else "N/A"}'
            )
            
            # Garantir que apenas uma imagem seja principal
            main_images = [img for img in images if img.is_main]
            if len(main_images) > 1:
                for i, img in enumerate(main_images):
                    if i > 0:
                        img.is_main = False
                        img.save()
            
            return response
    
    def update_client_relic_count(self, client):
        """Método auxiliar para atualizar estatísticas de relíquias do cliente"""
        relic_count = Relic.objects.filter(client=client).count()
        # Aqui poderíamos salvar em um campo específico se existisse
        return relic_count
    
    def create_adoption_availability_record(self, relic):
        """Método auxiliar para criar registro de disponibilidade para adoção"""
        # Criar uma adoção 'pendente' se a relíquia tem taxa de adoção
        if not Adoption.objects.filter(relic=relic, new_owner=relic.client).exists():
            Adoption.objects.create(
                relic=relic,
                new_owner=relic.client,
                previous_owner=relic.client,
                payment_status=False,
                created_by=self.request.user
            )

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

class RelicList(FilterView):
    model = Relic
    template_name = 'records/lists/relic.html'
    filterset_class = RelicFilter
    paginate_by = 12
    context_object_name = 'object_list'  # Usar object_list para compatibilidade
    
    def get_queryset(self):
        # Otimizar queries com select_related e prefetch_related
        qs = Relic.objects.select_related('client', 'created_by', 'client__address__city__state').prefetch_related('images')
        
        # Todos podem ver todas as relíquias para demonstração
        return qs.order_by('-obtained_date')
    
    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        
        # Calcular estatísticas TOTAIS do queryset completo (antes da paginação)
        filterset = self.get_filterset(self.filterset_class)
        total_queryset = filterset.qs
        context['total_relics'] = total_queryset.count()
        context['without_fee_count'] = total_queryset.filter(adoption_fee=0).count()
        context['with_fee_count'] = total_queryset.exclude(adoption_fee=0).count()
        context['unique_owners'] = total_queryset.values('client').distinct().count()
        
        # Adicionar alias para compatibilidade com template
        context['relics'] = context['object_list']
        
        return context

class AdoptionCreate(LoginRequiredMixin, CreateView):
    model = Adoption
    fields = ['relic', 'payment_status']
    template_name = 'records/form.html'
    success_url = reverse_lazy('records:AdoptionList')
    
    def form_valid(self, form):
        """Método form_valid que realiza múltiplas tarefas com outras classes do modelo"""
        
        # Usar transação para garantir consistência
        with transaction.atomic():
            # 1. Configurar dados básicos da adoção
            form.instance.created_by = self.request.user
            
            # 2. Automaticamente definir new_owner como o client_profile do usuário logado
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
            
            # 3. Salvar a adoção primeiro
            response = super().form_valid(form)
            adoption = form.instance
            
            # 4. MOVIMENTO PRINCIPAL: Transferir propriedade da relíquia
            if adoption.relic:
                old_owner = adoption.relic.client
                adoption.relic.client = adoption.new_owner
                adoption.relic.save()
                
                # 5. Atualizar last_activity dos clientes envolvidos
                adoption.new_owner.last_activity = timezone.now()
                adoption.new_owner.save()
                
                if old_owner != adoption.new_owner:
                    old_owner.last_activity = timezone.now()
                    old_owner.save()
                
                # 6. Criar registro de AdoptionRelic (histórico detalhado)
                AdoptionRelic.objects.create(
                    adoption=adoption,
                    relic=adoption.relic,
                    created_by=self.request.user
                )
                
                # 7. Adicionar mensagem de sucesso com detalhes
                messages.success(
                    self.request,
                    f'Adoção realizada com sucesso! '
                    f'A relíquia "{adoption.relic.name}" foi transferida '
                    f'de {old_owner.name} para {adoption.new_owner.name}.'
                )
                
                # 8. Se pagamento confirmado, atualizar status de todas as adoções da relíquia
                if adoption.payment_status:
                    Adoption.objects.filter(
                        relic=adoption.relic,
                        payment_status=False
                    ).update(payment_status=True)
            
            return response
    
    def get_form(self, form_class=None):
        form = super().get_form(form_class)
        # Filtrar apenas relíquias criadas pelo usuário atual
        form.fields['relic'].queryset = Relic.objects.filter(created_by=self.request.user)
        return form
    
    def update_client_statistics(self, client):
        """Método auxiliar para atualizar estatísticas do cliente"""
        # Contar quantas relíquias o cliente possui
        relics_count = Relic.objects.filter(client=client).count()
        
        # Contar quantas adoções o cliente fez (recebidas)
        adoptions_received = Adoption.objects.filter(new_owner=client).count()
        
        # Contar quantas adoções o cliente deu (doadas)
        adoptions_given = Adoption.objects.filter(previous_owner=client).count()
        
        # Atualizar last_activity
        client.last_activity = timezone.now()
        client.save()
        
        return {
            'relics_count': relics_count,
            'adoptions_received': adoptions_received,
            'adoptions_given': adoptions_given
        }

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
    paginate_by = 10
    
    def get_queryset(self):
        if self.request.user.is_authenticated:
            # Otimizar com select_related
            qs = Adoption.objects.select_related('new_owner', 'relic__client', 'created_by', 'relic')
            
            # Superusuários veem todas as adoções, usuários normais veem apenas as suas
            if self.request.user.is_superuser:
                return qs.order_by('-adoption_date')
            return qs.filter(created_by=self.request.user).order_by('-adoption_date')
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
    paginate_by = 10  # Paginação de 10 itens por página
    
    def get_queryset(self):
        if self.request.user.is_authenticated:
            return AdoptionRelic.objects.select_related(
                'adoption__new_owner', 
                'adoption__previous_owner', 
                'adoption__created_by',
                'relic__client',
                'relic__created_by',
                'created_by'
            ).filter(created_by=self.request.user).order_by('-id')
        return AdoptionRelic.objects.none()


class ProfileView(LoginRequiredMixin, ListView):
    model = Relic
    template_name = 'records/profile.html'
    context_object_name = 'user_relics'
    paginate_by = 6
    
    def get_queryset(self):
        return Relic.objects.select_related('client', 'created_by').prefetch_related('images').filter(created_by=self.request.user).order_by('-id')
    
    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        
        # Tentar obter o perfil do cliente com select_related otimizado
        try:
            client_profile = getattr(self.request.user, 'client_profile', None)
            if not client_profile:
                # Se não encontrar, procurar por clientes criados pelo usuário com otimização
                client_profile = Client.objects.select_related('address__city__state').filter(created_by=self.request.user).first()
        except:
            client_profile = None
            
        context['client_profile'] = client_profile
        context['total_relics'] = self.get_queryset().count()
        context['total_adoptions'] = Adoption.objects.filter(created_by=self.request.user).count()
        
        # Adicionar adoções do usuário com select_related otimizado (limitadas para não sobrecarregar)
        context['user_adoptions'] = Adoption.objects.select_related(
            'new_owner', 
            'previous_owner', 
            'relic__client', 
            'created_by'
        ).filter(created_by=self.request.user).order_by('-adoption_date')[:5]  # Apenas 5 mais recentes
        
        # Informações de paginação para as relíquias
        if hasattr(context, 'is_paginated') and context['is_paginated']:
            context['showing_count'] = len(context['object_list'])
        else:
            context['showing_count'] = context['total_relics']
        
        return context
