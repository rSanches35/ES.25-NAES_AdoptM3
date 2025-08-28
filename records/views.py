from django.views.generic.edit import CreateView, UpdateView, DeleteView
from django.views.generic.list import ListView

from django.urls import reverse_lazy
from .models import State, City, Address, Client, Relic, Adoption, AdoptionRelic

class StateCreate(CreateView):
    model = State
    fields = ['name', 'uf']
    template_name = 'records/form.html'
    success_url = reverse_lazy('pages-HomePage')

class StateUpdate(UpdateView):
    model = State
    fields = ['name', 'uf']
    template_name = 'records/form.html'
    success_url = reverse_lazy('pages-HomePage')

class StateDelete(DeleteView):
    model = State
    template_name = 'records/delete_confirm.html'
    success_url = reverse_lazy('pages-HomePage')

class StateList(ListView):
    model = State
    template_name = 'records/lists/state.html'



class CityCreate(CreateView):
    model = City
    fields = ['name', 'state']
    template_name = 'records/form.html'
    success_url = reverse_lazy('pages-HomePage')

class CityUpdate(UpdateView):
    model = City
    fields = ['name', 'state']
    template_name = 'records/form.html'
    success_url = reverse_lazy('pages-HomePage')

class CityDelete(DeleteView):
    model = City
    template_name = 'records/delete_confirm.html'
    success_url = reverse_lazy('pages-HomePage')

class CityList(ListView):
    model = City
    template_name = 'records/lists/city.html'



class AddressCreate(CreateView):
    model = Address
    fields = ['street', 'number', 'neighborhood', 'complement', 'city']
    template_name = 'records/form.html'
    success_url = reverse_lazy('pages-HomePage')

class AddressUpdate(UpdateView):
    model = Address
    fields = ['street', 'number', 'neighborhood', 'complement', 'city']
    template_name = 'records/form.html'
    success_url = reverse_lazy('pages-HomePage')

class AddressDelete(DeleteView):
    model = Address
    template_name = 'records/delete_confirm.html'
    success_url = reverse_lazy('pages-HomePage')

class AddressList(ListView):
    model = Address
    template_name = 'records/lists/address.html'



class ClientCreate(CreateView):
    model = Client
    fields = ['name', 'nickname', 'email', 'birth_date', 'register_date', 'last_activity', 'address']
    template_name = 'records/form.html'
    success_url = reverse_lazy('pages-HomePage')

class ClientUpdate(UpdateView):
    model = Client
    fields = ['name', 'nickname', 'email', 'birth_date', 'register_date', 'last_activity', 'address']
    template_name = 'records/form.html'
    success_url = reverse_lazy('pages-HomePage')

class ClientDelete(DeleteView):
    model = Client
    template_name = 'records/delete_confirm.html'
    success_url = reverse_lazy('pages-HomePage')

class ClientList(ListView):
    model = Client
    template_name = 'records/lists/client.html'



class RelicCreate(CreateView):
    model = Relic
    fields = ['name', 'description', 'obtained_date', 'adoption_fee', 'client']
    template_name = 'records/form.html'
    success_url = reverse_lazy('pages-HomePage')

class RelicUpdate(UpdateView):
    model = Relic
    fields = ['name', 'description', 'obtained_date', 'adoption_fee', 'client']
    template_name = 'records/form.html'
    success_url = reverse_lazy('pages-HomePage')

class RelicDelete(DeleteView):
    model = Relic
    template_name = 'records/delete_confirm.html'
    success_url = reverse_lazy('pages-HomePage')

class RelicList(ListView):
    model = Relic
    template_name = 'records/lists/relic.html'



class AdoptionCreate(CreateView):
    model = Adoption
    fields = ['adoption_date', 'payment_status', 'new_owner', 'previous_owner']
    template_name = 'records/form.html'
    success_url = reverse_lazy('pages-HomePage')

class AdoptionUpdate(UpdateView):
    model = Adoption
    fields = ['adoption_date', 'payment_status', 'new_owner', 'previous_owner']
    template_name = 'records/form.html'
    success_url = reverse_lazy('pages-HomePage')

class AdoptionDelete(DeleteView):
    model = Adoption
    template_name = 'records/delete_confirm.html'
    success_url = reverse_lazy('pages-HomePage')

class AdoptionList(ListView):
    model = Adoption
    template_name = 'records/lists/adoption.html'



class AdoptionRelicCreate(CreateView):
    model = AdoptionRelic
    fields = ['adoption', 'relic']
    template_name = 'records/form.html'
    success_url = reverse_lazy('pages-HomePage')

class AdoptionRelicUpdate(UpdateView):
    model = AdoptionRelic
    fields = ['adoption', 'relic']
    template_name = 'records/form.html'
    success_url = reverse_lazy('pages-HomePage')

class AdoptionRelicDelete(DeleteView):
    model = AdoptionRelic
    template_name = 'records/delete_confirm.html'
    success_url = reverse_lazy('pages-HomePage')

class AdoptionRelicList(ListView):
    model = AdoptionRelic
    template_name = 'records/lists/adoptionrelic.html'