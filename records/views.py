from django.views.generic.edit import CreateView, UpdateView, DeleteView
from django.views.generic.list import ListView
from django.contrib.auth.mixins import LoginRequiredMixin
from django.core.exceptions import PermissionDenied
from django.contrib.auth.views import LoginView
from django.contrib.auth import login
from django.shortcuts import render, redirect
from django.contrib import messages

from django.urls import reverse_lazy
from .models import State, City, Address, Client, Relic, Adoption, AdoptionRelic
from .forms import CustomUserCreationForm

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
    fields = ['user', 'name', 'nickname', 'birth_date', 'address']
    template_name = 'records/form.html'
    success_url = reverse_lazy('pages-HomePage')
    
    def get_queryset(self):
        return Client.objects.filter(created_by=self.request.user)
    
    def get_form(self, form_class=None):
        form = super().get_form(form_class)
        # Permitir o usuário atual ou usuários sem client_profile
        from django.contrib.auth.models import User
        current_user = self.object.user if self.object else None
        available_users = User.objects.filter(client_profile__isnull=True)
        if current_user:
            available_users = available_users | User.objects.filter(id=current_user.id)
        form.fields['user'].queryset = available_users
        return form

class ClientDelete(LoginRequiredMixin, DeleteView):
    model = Client
    template_name = 'records/delete_confirm.html'
    success_url = reverse_lazy('pages-HomePage')
    
    def get_queryset(self):
        return Client.objects.filter(created_by=self.request.user)

class ClientList(LoginRequiredMixin, ListView):
    model = Client
    template_name = 'records/lists/client.html'
    
    def get_queryset(self):
        return Client.objects.filter(created_by=self.request.user)



class RelicCreate(LoginRequiredMixin, CreateView):
    model = Relic
    fields = ['name', 'description', 'obtained_date', 'adoption_fee']
    template_name = 'records/form.html'
    success_url = reverse_lazy('pages-HomePage')
    
    def form_valid(self, form):
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
        
        return super().form_valid(form)

class RelicUpdate(LoginRequiredMixin, UpdateView):
    model = Relic
    fields = ['name', 'description', 'obtained_date', 'adoption_fee']
    template_name = 'records/form.html'
    success_url = reverse_lazy('pages-HomePage')
    
    def get_queryset(self):
        return Relic.objects.filter(created_by=self.request.user)

class RelicDelete(LoginRequiredMixin, DeleteView):
    model = Relic
    template_name = 'records/delete_confirm.html'
    success_url = reverse_lazy('pages-HomePage')
    
    def get_queryset(self):
        return Relic.objects.filter(created_by=self.request.user)

class RelicList(LoginRequiredMixin, ListView):
    model = Relic
    template_name = 'records/lists/relic.html'
    
    def get_queryset(self):
        return Relic.objects.filter(created_by=self.request.user)



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
        return Adoption.objects.filter(created_by=self.request.user)
    
    def get_form(self, form_class=None):
        form = super().get_form(form_class)
        # Filtrar apenas relíquias criadas pelo usuário atual
        form.fields['relic'].queryset = Relic.objects.filter(created_by=self.request.user)
        return form

class AdoptionDelete(LoginRequiredMixin, DeleteView):
    model = Adoption
    template_name = 'records/delete_confirm.html'
    success_url = reverse_lazy('records:AdoptionList')
    
    def get_queryset(self):
        return Adoption.objects.filter(created_by=self.request.user)

class AdoptionList(ListView):
    model = Adoption
    template_name = 'records/lists/adoption.html'
    context_object_name = 'adoptions'
    
    def get_queryset(self):
        if self.request.user.is_authenticated:
            return Adoption.objects.filter(created_by=self.request.user)
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