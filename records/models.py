from django.db import models
from django.contrib.auth.models import User

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