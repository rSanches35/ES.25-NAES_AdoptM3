from django.contrib import admin
from django.contrib.auth.models import Group, Permission
from django.contrib.contenttypes.models import ContentType

from .models import State, City, Address, Client, Relic, Adoption, AdoptionRelic

# Admin customizado para Client com controle por usuário
@admin.register(Client)
class ClientAdmin(admin.ModelAdmin):
    list_display = ['name', 'nickname', 'email', 'created_by']
    list_filter = ['created_by', 'register_date']
    
    def get_queryset(self, request):
        qs = super().get_queryset(request)
        if request.user.is_superuser:
            return qs
        return qs.filter(created_by=request.user)
    
    def save_model(self, request, obj, form, change):
        if not change:  # Se é um novo objeto
            obj.created_by = request.user
        super().save_model(request, obj, form, change)

# Admin customizado para Relic com controle por usuário
@admin.register(Relic)
class RelicAdmin(admin.ModelAdmin):
    list_display = ['name', 'description', 'client', 'created_by']
    list_filter = ['created_by', 'obtained_date']
    
    def get_queryset(self, request):
        qs = super().get_queryset(request)
        if request.user.is_superuser:
            return qs
        return qs.filter(created_by=request.user)
    
    def save_model(self, request, obj, form, change):
        if not change:  # Se é um novo objeto
            obj.created_by = request.user
        super().save_model(request, obj, form, change)

admin.site.register(State)
admin.site.register(City)
admin.site.register(Address)
admin.site.register(Adoption)
admin.site.register(AdoptionRelic)