from django.views.generic.edit import CreateView, UpdateView

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

    


class CityCreate(CreateView):
    model = City
    fields = ['name', 'state']
    template_name = 'records/form.html'
    success_url = reverse_lazy('pages-HomePage')

