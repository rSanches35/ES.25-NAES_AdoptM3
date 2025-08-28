from django.views.generic import TemplateView
from django.contrib.auth.forms import UserCreationForm
from django.contrib.auth import login
from django.shortcuts import render, redirect
from django.urls import reverse_lazy
from django.views.generic import CreateView
from django.contrib.auth.models import User
from django.db.models import Count, Q
from django.utils import timezone
from datetime import datetime, timedelta
from records.models import Client, Relic, Adoption

# Create your views here.
class IndexView(TemplateView):
    template_name = "pages/index.html"
    
    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        
        # Estatísticas gerais
        context['total_users'] = User.objects.count()
        context['total_clients'] = Client.objects.count()
        context['total_relics'] = Relic.objects.count()
        context['total_adoptions'] = Adoption.objects.count()
        
        # Últimos registros (se usuário logado)
        if self.request.user.is_authenticated:
            try:
                context['recent_clients'] = Client.objects.filter(
                    created_by=self.request.user
                ).order_by('-register_date')[:5]
                
                context['recent_relics'] = Relic.objects.filter(
                    created_by=self.request.user
                ).order_by('-obtained_date')[:5]
                
                context['user_stats'] = {
                    'my_clients': Client.objects.filter(created_by=self.request.user).count(),
                    'my_relics': Relic.objects.filter(created_by=self.request.user).count(),
                    'my_adoptions_given': Adoption.objects.filter(
                        previous_owner__created_by=self.request.user
                    ).count(),
                    'my_adoptions_received': Adoption.objects.filter(
                        new_owner__created_by=self.request.user
                    ).count(),
                }
            except Exception as e:
                # Em caso de erro, define valores padrão
                context['recent_clients'] = []
                context['recent_relics'] = []
                context['user_stats'] = {
                    'my_clients': 0,
                    'my_relics': 0,
                    'my_adoptions_given': 0,
                    'my_adoptions_received': 0,
                }
        else:
            # Dados públicos para usuários não logados
            try:
                context['recent_relics_public'] = Relic.objects.filter(
                    adoption_fee=False
                ).order_by('-obtained_date')[:3]
            except Exception as e:
                context['recent_relics_public'] = []
        
        return context

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