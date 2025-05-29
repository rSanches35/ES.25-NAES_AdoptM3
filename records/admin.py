from django.contrib import admin

from .models import State, City, Address, Client, Relic, Adoption, AdoptionRelic

admin.site.register(State)
admin.site.register(City)
admin.site.register(Address)
admin.site.register(Client)
admin.site.register(Relic)
admin.site.register(Adoption)
admin.site.register(AdoptionRelic)