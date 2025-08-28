from django.core.management.base import BaseCommand
from django.contrib.auth.models import Group, Permission
from django.contrib.contenttypes.models import ContentType
from records.models import Client, Relic

class Command(BaseCommand):
    help = 'Cria grupos de usuários com permissões específicas'

    def handle(self, *args, **options):
        # Criar grupos
        admin_group, created = Group.objects.get_or_create(name='Administradores')
        moderator_group, created = Group.objects.get_or_create(name='Moderadores')
        user_group, created = Group.objects.get_or_create(name='Usuários')

        # Permissões para Administradores (todas)
        admin_permissions = Permission.objects.all()
        admin_group.permissions.set(admin_permissions)

        # Permissões para Moderadores (ver todos, mas não deletar)
        client_ct = ContentType.objects.get_for_model(Client)
        relic_ct = ContentType.objects.get_for_model(Relic)
        
        moderator_permissions = Permission.objects.filter(
            content_type__in=[client_ct, relic_ct]
        ).exclude(codename__startswith='delete_')
        moderator_group.permissions.set(moderator_permissions)

        # Permissões para Usuários (apenas seus próprios dados)
        user_permissions = Permission.objects.filter(
            content_type__in=[client_ct, relic_ct],
            codename__in=['add_client', 'change_client', 'view_client', 
                         'add_relic', 'change_relic', 'view_relic']
        )
        user_group.permissions.set(user_permissions)

        self.stdout.write(
            self.style.SUCCESS('Grupos e permissões criados com sucesso!')
        )
