from django.db.models.signals import post_save
from django.dispatch import receiver
from django.contrib.auth.models import User
from .models import Client

@receiver(post_save, sender=User)
def create_or_update_client_profile(sender, instance, created, **kwargs):
    """
    Automaticamente cria um perfil de Cliente quando um novo usuário é criado
    ou atualiza o perfil existente quando o usuário é modificado
    """
    if created:
        # Usuário recém criado - criar perfil de cliente
        Client.objects.create(
            user=instance,
            name=instance.get_full_name() or instance.username,
            nickname=instance.username,
            email=instance.email,
            birth_date='1990-01-01',  # Data padrão - usuário pode atualizar depois
            created_by=instance
        )
    else:
        # Usuário existente - atualizar perfil se existir
        try:
            client = instance.client_profile
            # Sincronizar dados básicos
            client.email = instance.email
            if instance.get_full_name():
                client.name = instance.get_full_name()
            client.save()
        except Client.DoesNotExist:
            # Se não existir perfil, criar um
            Client.objects.create(
                user=instance,
                name=instance.get_full_name() or instance.username,
                nickname=instance.username,
                email=instance.email,
                birth_date='1990-01-01',  # Data padrão
                created_by=instance
            )
