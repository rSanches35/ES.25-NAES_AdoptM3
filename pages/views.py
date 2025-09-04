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
from django.contrib import messages
from records.forms import CustomUserCreationForm
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
    form_class = CustomUserCreationForm
    template_name = 'registration/signup.html'
    success_url = reverse_lazy('login')
    
    def form_valid(self, form):
        try:
            # Salva o usuário sem fazer login automático
            response = super().form_valid(form)
            print(f"Usuario criado com sucesso: {self.object.username}")
            print(f"Redirecionando para: {self.success_url}")
            
            # Adiciona mensagem de sucesso
            messages.success(
                self.request, 
                f'Conta criada com sucesso para {self.object.username}! Faça login para continuar.'
            )
            
            return response
        except Exception as e:
            # Debug: imprimir o erro
            print(f"Erro no signup: {e}")
            form.add_error(None, f"Erro ao criar conta: {str(e)}")
            return self.form_invalid(form)
    
    def form_invalid(self, form):
        # Debug: imprimir erros do formulário
        print(f"Erros do formulário: {form.errors}")
        return super().form_invalid(form)
    
    def get_success_url(self):
        print(f"get_success_url chamado, retornando: {self.success_url}")
        return str(self.success_url)