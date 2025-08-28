from django.contrib.auth.models import Group

class GroupMiddleware:
    """
    Middleware para adicionar o grupo do usuário ao contexto da requisição
    """
    def __init__(self, get_response):
        self.get_response = get_response

    def __call__(self, request):
        if hasattr(request, 'user') and request.user.is_authenticated:
            try:
                # Adiciona o grupo principal do usuário
                user_groups = request.user.groups.all()
                if user_groups.exists():
                    request.user_group = user_groups.first().name
                else:
                    # Se não tem grupo, adiciona ao grupo "Usuários" por padrão
                    user_group, created = Group.objects.get_or_create(name='Usuários')
                    request.user.groups.add(user_group)
                    request.user_group = 'Usuários'
            except Exception as e:
                # Em caso de erro, define como None
                request.user_group = None
        else:
            request.user_group = None

        response = self.get_response(request)
        return response
