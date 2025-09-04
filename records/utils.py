from django.shortcuts import redirect
from django.contrib import messages
from django.contrib.auth.decorators import login_required
from .models import Client

@login_required
def create_client_profile(request):
    """
    Cria automaticamente um perfil de cliente para o usuário logado
    se ele ainda não tiver um.
    """
    user = request.user
    
    # Verificar se o usuário já tem um client_profile
    if hasattr(user, 'client_profile') and user.client_profile:
        messages.info(request, 'Você já possui um perfil de cliente.')
        return redirect('pages-HomePage')
    
    # Verificar se já existe um cliente para este usuário
    existing_client = Client.objects.filter(user=user).first()
    if existing_client:
        messages.info(request, 'Você já possui um perfil de cliente.')
        return redirect('pages-HomePage')
    
    # Criar novo perfil de cliente
    try:
        client = Client.objects.create(
            user=user,
            name=user.get_full_name() or user.username,
            nickname=user.username,
            email=user.email,
            birth_date='1990-01-01',  # Data padrão - usuário pode atualizar depois
            created_by=user
        )
        messages.success(request, f'Perfil de cliente criado com sucesso para {client.name}!')
    except Exception as e:
        messages.error(request, f'Erro ao criar perfil de cliente: {str(e)}')
    
    return redirect('pages-HomePage')
