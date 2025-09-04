from django.db import models
from django.contrib.auth.models import User
import os
from uuid import uuid4

# Função para definir o caminho de upload das fotos de perfil dos clientes
def client_photo_upload_path(instance, filename):
    ext = filename.split('.')[-1]
    filename = f'{uuid4().hex}.{ext}'
    return os.path.join('clients', 'profile_photos', filename)

# Função para definir o caminho de upload das imagens das relíquias
def relic_image_upload_path(instance, filename):
    ext = filename.split('.')[-1]
    filename = f'{uuid4().hex}.{ext}'
    return os.path.join('relics', 'images', filename)

# -Classe Estado
class State(models.Model):
    name = models.CharField(max_length=80)
    uf = models.CharField(max_length=2)

    def __str__(self):
        return "{} - {}".format(self.name, self.uf)

# -Classe Cidade
class City(models.Model):
    name = models.CharField(max_length=150)
    state = models.ForeignKey(State, on_delete=models.PROTECT)

    def __str__(self):
        return "{}, {}".format(self.name, self.state.name)
    
# -Classe Endereço
class Address(models.Model):
    street = models.CharField(max_length=150)
    number = models.IntegerField()
    neighborhood = models.CharField(max_length=150)
    complement = models.CharField(max_length=100)
    city = models.ForeignKey(City, on_delete=models.PROTECT)

    def __str__(self):
        return "{}, {}. \n{} n{}°, {}".format(self.city.state.name, self.city.name, self.street, self.number, self.neighborhood)
    
# -Classe CLiente
class Client(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE, related_name='client_profile', null=True, blank=True)
    name = models.CharField(max_length=150)
    nickname = models.CharField(max_length=50)
    email = models.EmailField()
    birth_date = models.DateField()
    profile_photo = models.ImageField(
        upload_to=client_photo_upload_path, 
        null=True, 
        blank=True,
        help_text='Foto de perfil do cliente (opcional)'
    )
    register_date = models.DateTimeField(auto_now_add=True)
    last_activity = models.DateTimeField(auto_now=True)
    address = models.ForeignKey(Address, on_delete=models.PROTECT, null=True, blank=True)
    created_by = models.ForeignKey(User, on_delete=models.CASCADE, related_name='clients', default=1)

    def save(self, *args, **kwargs):
        # Automaticamente sincronizar email com o usuário Django
        if self.user:
            self.email = self.user.email
            if not self.name and self.user.get_full_name():
                self.name = self.user.get_full_name()
            if not self.nickname:
                self.nickname = self.user.username
        super().save(*args, **kwargs)

    def __str__(self):
        user_info = f" ({self.user.username})" if self.user else ""
        return "{}{}, [{}] \n{}".format(self.name, user_info, self.nickname, self.last_activity)
    
# -Classe Relíquia
class Relic(models.Model):
    name = models.CharField(max_length=150, default='')
    description = models.CharField(max_length=500, default='')
    obtained_date = models.DateField(null=True, blank=True)
    adoption_fee = models.BooleanField(default=False)
    client = models.ForeignKey(Client, on_delete=models.PROTECT)
    created_by = models.ForeignKey(User, on_delete=models.CASCADE, related_name='relics', default=1)

    def __str__(self):
        return "{}, {}".format(self.name, self.description)

    def get_main_image(self):
        """Retorna a primeira imagem da relíquia (imagem principal)"""
        first_image = self.images.first()
        return first_image.image if first_image else None

    def get_all_images(self):
        """Retorna todas as imagens da relíquia"""
        return self.images.all()

# -Classe Imagem da Relíquia
class RelicImage(models.Model):
    relic = models.ForeignKey(Relic, on_delete=models.CASCADE, related_name='images')
    image = models.ImageField(
        upload_to=relic_image_upload_path,
        help_text='Imagem da relíquia'
    )
    is_main = models.BooleanField(
        default=False,
        help_text='Marcar como imagem principal'
    )
    upload_date = models.DateTimeField(auto_now_add=True)
    created_by = models.ForeignKey(User, on_delete=models.CASCADE, related_name='relic_images', default=1)

    class Meta:
        ordering = ['-is_main', 'upload_date']
        verbose_name = 'Imagem da Relíquia'
        verbose_name_plural = 'Imagens das Relíquias'

    def __str__(self):
        main_text = " (Principal)" if self.is_main else ""
        return f"Imagem de {self.relic.name}{main_text}"

    def save(self, *args, **kwargs):
        # Se esta imagem está sendo marcada como principal, desmarcar as outras
        if self.is_main:
            RelicImage.objects.filter(relic=self.relic, is_main=True).update(is_main=False)
        super().save(*args, **kwargs)
    
# -Classe Adoção
class Adoption(models.Model):
    adoption_date = models.DateField(auto_now_add=True)
    payment_status = models.BooleanField(default=False)
    relic = models.ForeignKey(Relic, on_delete=models.PROTECT, related_name='adoptions', null=True, blank=True)
    new_owner = models.ForeignKey(Client, on_delete=models.PROTECT, related_name='adoptions_received')
    previous_owner = models.ForeignKey(Client, on_delete=models.PROTECT, related_name='adoptions_given')
    created_by = models.ForeignKey(User, on_delete=models.CASCADE, related_name='adoptions', default=1)

    def save(self, *args, **kwargs):
        # Automatically set previous_owner from the relic's client
        if self.relic and not self.previous_owner_id:
            self.previous_owner = self.relic.client
        super().save(*args, **kwargs)

    def __str__(self):
        relic_name = self.relic.name if self.relic else "Sem relíquia"
        return "Adoção de {} - {} para {}".format(relic_name, self.previous_owner.name, self.new_owner.name)
    
# -Classe AdoçãoRelíquia (DEPRECIADA - agora a relação é direta no modelo Adoption)
class AdoptionRelic(models.Model):
    adoption = models.ForeignKey(Adoption, on_delete=models.PROTECT)
    relic = models.ForeignKey(Relic, on_delete=models.PROTECT)
    created_by = models.ForeignKey(User, on_delete=models.CASCADE, related_name='adoption_relics', default=1)

    def __str__(self):
        return "{}, {}".format(self.adoption.adoption_date, self.relic.name)
    
    class Meta:
        verbose_name = "Adoção-Relíquia (Depreciado)"
        verbose_name_plural = "Adoções-Relíquias (Depreciado)"