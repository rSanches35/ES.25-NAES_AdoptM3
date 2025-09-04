from django.contrib import admin
from django.contrib.auth.models import Group, Permission, User
from django.contrib.contenttypes.models import ContentType

from .models import State, City, Address, Client, Relic, Adoption, AdoptionRelic, RelicImage

# Admin customizado para Client com controle por usuário
@admin.register(Client)
class ClientAdmin(admin.ModelAdmin):
    list_display = ['name', 'nickname', 'user', 'email', 'created_by']
    list_filter = ['created_by', 'register_date']
    fields = ['user', 'name', 'nickname', 'birth_date', 'profile_photo', 'address']  # Adicionado profile_photo
    readonly_fields = ['email']  # Email é somente leitura pois vem do User
    
    def get_queryset(self, request):
        qs = super().get_queryset(request)
        if request.user.is_superuser:
            return qs
        return qs.filter(created_by=request.user)
    
    def formfield_for_foreignkey(self, db_field, request, **kwargs):
        if db_field.name == "user":
            # Mostrar apenas usuários que ainda não têm um client_profile
            kwargs["queryset"] = User.objects.filter(client_profile__isnull=True)
        return super().formfield_for_foreignkey(db_field, request, **kwargs)
    
    def save_model(self, request, obj, form, change):
        if not change:  # Se é um novo objeto
            obj.created_by = request.user
        super().save_model(request, obj, form, change)

# Inline para imagens das relíquias
class RelicImageInline(admin.TabularInline):
    model = RelicImage
    extra = 1
    max_num = 5  # Máximo de 5 imagens
    fields = ['image', 'is_main']
    readonly_fields = ['upload_date']
    
    def save_model(self, request, obj, form, change):
        if not change:  # Se é um novo objeto
            obj.created_by = request.user
        super().save_model(request, obj, form, change)

# Admin customizado para Relic com controle por usuário
@admin.register(Relic)
class RelicAdmin(admin.ModelAdmin):
    list_display = ['name', 'description', 'client', 'created_by']
    list_filter = ['created_by', 'obtained_date']
    fields = ['name', 'description', 'obtained_date', 'adoption_fee']  # Removendo client dos campos editáveis
    readonly_fields = ['client']  # Client será somente leitura
    inlines = [RelicImageInline]  # Adicionado inline para imagens
    
    def get_queryset(self, request):
        qs = super().get_queryset(request)
        if request.user.is_superuser:
            return qs
        return qs.filter(created_by=request.user)
    
    def formfield_for_foreignkey(self, db_field, request, **kwargs):
        if db_field.name == "client":
            # Filtrar apenas clientes criados pelo usuário atual
            kwargs["queryset"] = Client.objects.filter(created_by=request.user)
        return super().formfield_for_foreignkey(db_field, request, **kwargs)
    
    def save_model(self, request, obj, form, change):
        if not change:  # Se é um novo objeto
            obj.created_by = request.user
            # Buscar automaticamente um cliente do usuário logado
            try:
                # Primeiro tenta encontrar o client_profile do usuário
                user_client = getattr(request.user, 'client_profile', None)
                if not user_client:
                    # Se não encontrar, criar um cliente automaticamente para o usuário
                    user_client = Client.objects.create(
                        user=request.user,
                        name=request.user.get_full_name() or request.user.username,
                        nickname=request.user.username,
                        email=request.user.email,
                        birth_date='1990-01-01',  # Data padrão - pode ser ajustada depois
                        created_by=request.user
                    )
                obj.client = user_client
            except Exception as e:
                # Em caso de erro, tentar encontrar qualquer cliente do usuário
                user_client = Client.objects.filter(created_by=request.user).first()
                if user_client:
                    obj.client = user_client
        super().save_model(request, obj, form, change)

# Admin customizado para Adoption com controle por usuário
@admin.register(Adoption)
class AdoptionAdmin(admin.ModelAdmin):
    list_display = ['relic', 'previous_owner', 'new_owner', 'adoption_date', 'payment_status', 'created_by']
    list_filter = ['created_by', 'adoption_date', 'payment_status']
    fields = ['relic', 'payment_status']  # Apenas relic e payment_status são editáveis
    readonly_fields = ['adoption_date', 'new_owner', 'previous_owner']  # Campos automáticos
    
    def get_queryset(self, request):
        qs = super().get_queryset(request)
        if request.user.is_superuser:
            return qs
        return qs.filter(created_by=request.user)
    
    def formfield_for_foreignkey(self, db_field, request, **kwargs):
        if db_field.name == "relic":
            # Filtrar apenas relíquias criadas pelo usuário atual
            kwargs["queryset"] = Relic.objects.filter(created_by=request.user)
        return super().formfield_for_foreignkey(db_field, request, **kwargs)
    
    def save_model(self, request, obj, form, change):
        if not change:  # Se é um novo objeto
            obj.created_by = request.user
            
            # Buscar automaticamente um cliente do usuário logado para new_owner
            try:
                # Primeiro tenta encontrar o client_profile do usuário
                user_client = getattr(request.user, 'client_profile', None)
                if not user_client:
                    # Se não encontrar, criar um cliente automaticamente para o usuário
                    user_client = Client.objects.create(
                        user=request.user,
                        name=request.user.get_full_name() or request.user.username,
                        nickname=request.user.username,
                        email=request.user.email,
                        birth_date='1990-01-01',  # Data padrão - pode ser ajustada depois
                        created_by=request.user
                    )
                obj.new_owner = user_client
            except Exception as e:
                # Em caso de erro, tentar encontrar qualquer cliente do usuário
                user_client = Client.objects.filter(created_by=request.user).first()
                if user_client:
                    obj.new_owner = user_client
        
        # O previous_owner será definido automaticamente pelo método save() do modelo
        super().save_model(request, obj, form, change)

admin.site.register(State)
admin.site.register(City)
admin.site.register(Address)
admin.site.register(AdoptionRelic)

# Admin customizado para RelicImage
@admin.register(RelicImage)
class RelicImageAdmin(admin.ModelAdmin):
    list_display = ['relic', 'is_main', 'upload_date', 'created_by']
    list_filter = ['is_main', 'upload_date', 'created_by']
    fields = ['relic', 'image', 'is_main']
    readonly_fields = ['upload_date']
    
    def get_queryset(self, request):
        qs = super().get_queryset(request)
        if request.user.is_superuser:
            return qs
        return qs.filter(created_by=request.user)
    
    def formfield_for_foreignkey(self, db_field, request, **kwargs):
        if db_field.name == "relic":
            # Filtrar apenas relíquias criadas pelo usuário atual
            kwargs["queryset"] = Relic.objects.filter(created_by=request.user)
        return super().formfield_for_foreignkey(db_field, request, **kwargs)
    
    def save_model(self, request, obj, form, change):
        if not change:  # Se é um novo objeto
            obj.created_by = request.user
        super().save_model(request, obj, form, change)