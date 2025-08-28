from django.views.generic.edit import CreateView, UpdateView, DeleteView
from django.views.generic.list import ListView
from django.contrib.auth.mixins import LoginRequiredMixin
from django.core.exceptions import PermissionDenied

from django.urls import reverse_lazy
from .models import State, City, Address, Client, Relic, Adoption, AdoptionRelic

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
    fields = ['name', 'nickname', 'email', 'birth_date', 'register_date', 'last_activity', 'address']
    template_name = 'records/form.html'
    success_url = reverse_lazy('pages-HomePage')
    
    def form_valid(self, form):
        form.instance.created_by = self.request.user
        return super().form_valid(form)

class ClientUpdate(LoginRequiredMixin, UpdateView):
    model = Client
    fields = ['name', 'nickname', 'email', 'birth_date', 'register_date', 'last_activity', 'address']
    template_name = 'records/form.html'
    success_url = reverse_lazy('pages-HomePage')
    
    def get_queryset(self):
        return Client.objects.filter(created_by=self.request.user)

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
    fields = ['name', 'description', 'obtained_date', 'adoption_fee', 'client']
    template_name = 'records/form.html'
    success_url = reverse_lazy('pages-HomePage')
    
    def form_valid(self, form):
        form.instance.created_by = self.request.user
        return super().form_valid(form)

class RelicUpdate(LoginRequiredMixin, UpdateView):
    model = Relic
    fields = ['name', 'description', 'obtained_date', 'adoption_fee', 'client']
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
    fields = ['adoption_date', 'payment_status', 'new_owner', 'previous_owner']
    template_name = 'records/form.html'
    success_url = reverse_lazy('records:AdoptionList')
    
    def form_valid(self, form):
        form.instance.created_by = self.request.user
        return super().form_valid(form)

class AdoptionUpdate(LoginRequiredMixin, UpdateView):
    model = Adoption
    fields = ['adoption_date', 'payment_status', 'new_owner', 'previous_owner']
    template_name = 'records/form.html'
    success_url = reverse_lazy('records:AdoptionList')
    
    def get_queryset(self):
        return Adoption.objects.filter(created_by=self.request.user)

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