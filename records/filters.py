import django_filters
from django import forms
from django.db.models import Q
from .models import Client, Relic, State, City


class ClientFilter(django_filters.FilterSet):
    """
    Filtro para a lista de clientes com lookups: icontains, exact, gte, lte
    """
    # Filtro por nome (icontains - busca parcial case-insensitive)
    name = django_filters.CharFilter(
        field_name='name',
        lookup_expr='icontains',
        label='Nome',
        widget=forms.TextInput(attrs={
            'class': 'form-control',
            'placeholder': 'Digite o nome do cliente...'
        })
    )
    
    # Filtro por apelido (icontains)
    nickname = django_filters.CharFilter(
        field_name='nickname',
        lookup_expr='icontains',
        label='Apelido',
        widget=forms.TextInput(attrs={
            'class': 'form-control',
            'placeholder': 'Digite o apelido...'
        })
    )
    
    # Filtro por email (icontains)
    email = django_filters.CharFilter(
        field_name='email',
        lookup_expr='icontains',
        label='Email',
        widget=forms.EmailInput(attrs={
            'class': 'form-control',
            'placeholder': 'Digite o email...'
        })
    )
    
    # Filtro por data de nascimento - maior ou igual (gte)
    birth_date_after = django_filters.DateFilter(
        field_name='birth_date',
        lookup_expr='gte',
        label='Nasceu após',
        widget=forms.DateInput(attrs={
            'class': 'form-control',
            'type': 'date'
        })
    )
    
    # Filtro por data de nascimento - menor ou igual (lte)
    birth_date_before = django_filters.DateFilter(
        field_name='birth_date',
        lookup_expr='lte',
        label='Nasceu antes',
        widget=forms.DateInput(attrs={
            'class': 'form-control',
            'type': 'date'
        })
    )
    
    # Filtro por data de registro - maior ou igual (gte)
    register_date_after = django_filters.DateFilter(
        field_name='register_date',
        lookup_expr='gte',
        label='Registrado após',
        widget=forms.DateInput(attrs={
            'class': 'form-control',
            'type': 'date'
        })
    )
    
    # Filtro por data de registro - menor ou igual (lte)
    register_date_before = django_filters.DateFilter(
        field_name='register_date',
        lookup_expr='lte',
        label='Registrado antes',
        widget=forms.DateInput(attrs={
            'class': 'form-control',
            'type': 'date'
        })
    )
    
    # Filtro por usuário criador (exact)
    created_by = django_filters.ModelChoiceFilter(
        field_name='created_by',
        lookup_expr='exact',
        label='Criado por',
        queryset=None,  # Será definido no __init__
        widget=forms.Select(attrs={'class': 'form-control'})
    )
    
    class Meta:
        model = Client
        fields = []
    
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        # Definir queryset dos usuários criadores
        from django.contrib.auth.models import User
        self.filters['created_by'].queryset = User.objects.filter(
            clients__isnull=False
        ).distinct()


class RelicFilter(django_filters.FilterSet):
    """
    Filtro para a lista de relíquias com lookups: icontains, exact, gte, lte
    """
    # Filtro por nome da relíquia (icontains)
    name = django_filters.CharFilter(
        field_name='name',
        lookup_expr='icontains',
        label='Nome da Relíquia',
        widget=forms.TextInput(attrs={
            'class': 'form-control',
            'placeholder': 'Digite o nome da relíquia...'
        })
    )
    
    # Filtro por descrição (icontains)
    description = django_filters.CharFilter(
        field_name='description',
        lookup_expr='icontains',
        label='Descrição',
        widget=forms.TextInput(attrs={
            'class': 'form-control',
            'placeholder': 'Digite palavras da descrição...'
        })
    )
    
    # Filtro por taxa de adoção (com método personalizado)
    adoption_fee = django_filters.ChoiceFilter(
        field_name='adoption_fee',
        label='Possui taxa de adoção',
        choices=[
            ('', 'Todos'),
            ('true', 'Sim'),
            ('false', 'Não'),
        ],
        widget=forms.Select(attrs={'class': 'form-control'}),
        method='filter_adoption_fee'
    )
    
    # Filtro por data de obtenção - a partir de (gte)
    obtained_date_after = django_filters.DateFilter(
        field_name='obtained_date',
        lookup_expr='gte',
        label='Obtida após',
        widget=forms.DateInput(attrs={
            'class': 'form-control',
            'type': 'date'
        })
    )
    
    # Filtro por data de obtenção - até (lte)
    obtained_date_before = django_filters.DateFilter(
        field_name='obtained_date',
        lookup_expr='lte',
        label='Obtida antes',
        widget=forms.DateInput(attrs={
            'class': 'form-control',
            'type': 'date'
        })
    )
    
    # Filtro por proprietário (exact)
    client = django_filters.ModelChoiceFilter(
        field_name='client',
        lookup_expr='exact',
        label='Proprietário',
        queryset=Client.objects.all(),
        widget=forms.Select(attrs={'class': 'form-control'})
    )
    
    # Filtro por usuário criador (exact)
    created_by = django_filters.ModelChoiceFilter(
        field_name='created_by',
        lookup_expr='exact',
        label='Criado por',
        queryset=None,  # Será definido no __init__
        widget=forms.Select(attrs={'class': 'form-control'})
    )
    

    
    class Meta:
        model = Relic
        fields = []
    
    def filter_adoption_fee(self, queryset, name, value):
        """
        Método personalizado para filtrar por taxa de adoção.
        Converte strings 'true'/'false' para valores booleanos.
        """
        if value == 'true':
            return queryset.filter(adoption_fee=True)
        elif value == 'false':
            return queryset.filter(adoption_fee=False)
        # Se value é '' ou None, retorna todos os registros
        return queryset
    
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        # Definir queryset dos usuários criadores
        from django.contrib.auth.models import User
        self.filters['created_by'].queryset = User.objects.filter(
            relics__isnull=False
        ).distinct()
        
        # Otimizar queryset dos clientes
        self.filters['client'].queryset = Client.objects.select_related('user').all()