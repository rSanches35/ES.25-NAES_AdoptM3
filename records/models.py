from django.db import models

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
    name = models.CharField(max_length=150)
    nickname = models.CharField(max_length=50)
    email = models.EmailField()
    birth_date = models.DateField()
    register_date = models.DateTimeField()
    last_activity = models.DateTimeField()
    address = models.ForeignKey(Address, on_delete=models.PROTECT)

    def __str__(self):
        return "{}, [{}] \n{}".format(self.name, self.nickname, self.last_activity)
    
# -Classe Relíquia
class Relic(models.Model):
    name = models.CharField(max_length=150),
    description = models.CharField(max_length=500),
    obtained_date = models.DateField(),
    adoption_fee = models.BooleanField(),
    client = models.ForeignKey(Client, on_delete=models.PROTECT)

    def __str__(self):
        return "{}, {}".format(self.name, self.description)
    
# -Classe Relíquia
class Adoption(models.Model):
    adoption_date = models.DateField()
    payment_status = models.CharField(max_length=50)
    new_owner = models.ForeignKey(Client, on_delete=models.PROTECT, related_name='adoptions_received')
    previous_owner = models.ForeignKey(Client, on_delete=models.PROTECT, related_name='adoptions_given')

    def __str__(self):
        return "{}, {}".format(self.previous_owner.name, self.new_owner.name)
    
# -Classe AdoçãoRelíquia
class AdoptionRelic(models.Model):
    adoption = models.ForeignKey(Adoption, on_delete=models.PROTECT)
    relic = models.ForeignKey(Relic, on_delete=models.PROTECT)

    def __str__(self):
        return "{}, {}".format(self.adoption.adoption_date, self.relic.name)