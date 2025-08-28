from django.views.generic import TemplateView
from django.contrib.auth.forms import UserCreationForm
from django.contrib.auth import login
from django.shortcuts import render, redirect
from django.urls import reverse_lazy
from django.views.generic import CreateView
from django.contrib.auth.models import User

# Create your views here.
class IndexView(TemplateView):
    
    template_name = "pages/index.html"

class AboutView(TemplateView):
    
    template_name = "pages/about.html"

class SignUpView(CreateView):
    model = User
    form_class = UserCreationForm
    template_name = 'registration/signup.html'
    success_url = reverse_lazy('login')
    
    def form_valid(self, form):
        response = super().form_valid(form)
        # Login automático após cadastro
        login(self.request, self.object)
        return response