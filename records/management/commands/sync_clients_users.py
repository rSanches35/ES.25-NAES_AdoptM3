from django.core.management.base import BaseCommand
from django.contrib.auth.models import User
from records.models import Client

class Command(BaseCommand):
    help = 'Sincroniza clientes existentes com usuários Django'

    def handle(self, *args, **options):
        # Encontrar clientes sem usuário vinculado
        clients_without_user = Client.objects.filter(user__isnull=True)
        
        self.stdout.write(f"Encontrados {clients_without_user.count()} clientes sem usuário vinculado")
        
        for client in clients_without_user:
            # Tentar encontrar um usuário com o mesmo email
            try:
                user = User.objects.get(email=client.email)
                client.user = user
                client.save()
                self.stdout.write(
                    self.style.SUCCESS(f"Cliente '{client.name}' vinculado ao usuário '{user.username}'")
                )
            except User.DoesNotExist:
                # Criar um novo usuário para este cliente
                username = client.nickname or client.email.split('@')[0]
                # Garantir que o username seja único
                counter = 1
                original_username = username
                while User.objects.filter(username=username).exists():
                    username = f"{original_username}{counter}"
                    counter += 1
                
                user = User.objects.create_user(
                    username=username,
                    email=client.email,
                    first_name=client.name.split()[0] if client.name else '',
                    last_name=' '.join(client.name.split()[1:]) if len(client.name.split()) > 1 else ''
                )
                
                client.user = user
                client.save()
                self.stdout.write(
                    self.style.WARNING(f"Criado novo usuário '{user.username}' para cliente '{client.name}'")
                )
            except User.MultipleObjectsReturned:
                # Se houver múltiplos usuários com o mesmo email, usar o primeiro
                user = User.objects.filter(email=client.email).first()
                client.user = user
                client.save()
                self.stdout.write(
                    self.style.WARNING(f"Cliente '{client.name}' vinculado ao primeiro usuário com email '{client.email}'")
                )
        
        self.stdout.write(
            self.style.SUCCESS(f"Sincronização concluída! {clients_without_user.count()} clientes processados.")
        )
