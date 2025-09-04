from django import forms
from django.contrib.auth.forms import UserCreationForm
from django.contrib.auth.models import User
from .models import Client, Relic, RelicImage

class CustomUserCreationForm(UserCreationForm):
    email = forms.EmailField(
        required=True,
        help_text='Obrigatório. Informe um endereço de e-mail válido.'
    )
    name = forms.CharField(
        max_length=150,
        required=True,
        help_text='Obrigatório. Seu nome completo.'
    )
    birth_date = forms.DateField(
        required=True,
        widget=forms.DateInput(attrs={'type': 'date'}),
        help_text='Obrigatório. Sua data de nascimento.'
    )

    class Meta:
        model = User
        fields = ('username', 'email', 'password1', 'password2')

    def clean_email(self):
        email = self.cleaned_data.get('email')
        if User.objects.filter(email=email).exists():
            raise forms.ValidationError('Este e-mail já está sendo usado por outro usuário.')
        return email

    def save(self, commit=True):
        user = super().save(commit=False)
        user.email = self.cleaned_data['email']
        
        # Dividir o nome em first_name e last_name
        name_parts = self.cleaned_data['name'].strip().split()
        if name_parts:
            user.first_name = name_parts[0]
            user.last_name = ' '.join(name_parts[1:]) if len(name_parts) > 1 else ''
        
        if commit:
            user.save()
            # Criar automaticamente o perfil de Cliente apenas se não existir
            if not Client.objects.filter(user=user).exists():
                Client.objects.create(
                    user=user,
                    name=self.cleaned_data['name'],
                    nickname=user.username,
                    email=user.email,
                    birth_date=self.cleaned_data['birth_date'],
                    created_by=user
                )
        
        return user

class ClientEditForm(forms.ModelForm):
    """Formulário para edição de cliente, incluindo foto de perfil"""
    class Meta:
        model = Client
        fields = ['name', 'nickname', 'birth_date', 'profile_photo', 'address']
        widgets = {
            'name': forms.TextInput(attrs={'class': 'form-control', 'placeholder': 'Nome completo'}),
            'nickname': forms.TextInput(attrs={'class': 'form-control', 'placeholder': 'Apelido'}),
            'birth_date': forms.DateInput(attrs={'type': 'date', 'class': 'form-control'}),
            'profile_photo': forms.FileInput(attrs={'class': 'form-control', 'accept': 'image/*'}),
        }
    
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.fields['profile_photo'].help_text = 'Selecione uma imagem para seu perfil (opcional)'
    
    def clean_profile_photo(self):
        """Validação personalizada para a foto de perfil"""
        photo = self.cleaned_data.get('profile_photo')
        if photo:
            # Verificar tamanho do arquivo (max 5MB)
            if photo.size > 5 * 1024 * 1024:
                raise forms.ValidationError('O arquivo é muito grande. Tamanho máximo: 5MB')
            
            # Verificar tipo de arquivo
            valid_types = ['image/jpeg', 'image/jpg', 'image/png', 'image/gif', 'image/webp']
            if hasattr(photo, 'content_type') and photo.content_type not in valid_types:
                raise forms.ValidationError('Tipo de arquivo inválido. Use: JPG, PNG, GIF ou WebP')
            
            # Verificar extensão do nome do arquivo
            import os
            name, ext = os.path.splitext(photo.name)
            if ext.lower() not in ['.jpg', '.jpeg', '.png', '.gif', '.webp']:
                raise forms.ValidationError('Extensão de arquivo inválida. Use: .jpg, .png, .gif ou .webp')
            
            # Verificar se o nome do arquivo não é muito longo
            if len(photo.name) > 100:
                raise forms.ValidationError('Nome do arquivo muito longo. Use um nome mais curto.')
        
        return photo

class RelicCreateForm(forms.ModelForm):
    """Formulário para criação de relíquia (sem imagens - serão adicionadas depois)"""
    class Meta:
        model = Relic
        fields = ['name', 'description', 'obtained_date', 'adoption_fee']
        widgets = {
            'name': forms.TextInput(attrs={'class': 'form-control', 'placeholder': 'Nome da relíquia'}),
            'description': forms.Textarea(attrs={
                'class': 'form-control', 
                'placeholder': 'Descrição da relíquia',
                'rows': 4
            }),
            'obtained_date': forms.DateInput(attrs={'type': 'date', 'class': 'form-control'}),
            'adoption_fee': forms.CheckboxInput(attrs={'class': 'form-check-input'}),
        }

class RelicImageForm(forms.ModelForm):
    """Formulário para upload de imagens das relíquias"""
    class Meta:
        model = RelicImage
        fields = ['image', 'is_main']
        widgets = {
            'image': forms.FileInput(attrs={
                'class': 'form-control', 
                'accept': 'image/*',
                'multiple': False
            }),
            'is_main': forms.CheckboxInput(attrs={'class': 'form-check-input'}),
        }
    
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.fields['image'].help_text = 'Selecione uma imagem da relíquia'
        self.fields['is_main'].help_text = 'Marcar como imagem principal'
    
    def clean_image(self):
        """Validação personalizada para as imagens das relíquias"""
        image = self.cleaned_data.get('image')
        if image:
            # Verificar tamanho do arquivo (max 10MB para relíquias)
            if image.size > 10 * 1024 * 1024:
                raise forms.ValidationError('O arquivo é muito grande. Tamanho máximo: 10MB')
            
            # Verificar tipo de arquivo
            valid_types = ['image/jpeg', 'image/jpg', 'image/png', 'image/gif', 'image/webp']
            if hasattr(image, 'content_type') and image.content_type not in valid_types:
                raise forms.ValidationError('Tipo de arquivo inválido. Use: JPG, PNG, GIF ou WebP')
            
            # Verificar extensão do nome do arquivo
            import os
            name, ext = os.path.splitext(image.name)
            if ext.lower() not in ['.jpg', '.jpeg', '.png', '.gif', '.webp']:
                raise forms.ValidationError('Extensão de arquivo inválida. Use: .jpg, .png, .gif ou .webp')
            
            # Verificar se o nome do arquivo não é muito longo
            if len(image.name) > 100:
                raise forms.ValidationError('Nome do arquivo muito longo. Use um nome mais curto.')
        
        return image

# Formset para múltiplas imagens de relíquia
RelicImageFormSet = forms.modelformset_factory(
    RelicImage,
    form=RelicImageForm,
    extra=1,  # Começar com 1 formulário vazio
    max_num=5,  # Máximo de 5 imagens
    min_num=0,  # Mínimo de 0 imagens (vamos validar manualmente)
    validate_min=False,  # Não validar automaticamente, faremos validação customizada
    can_delete=True
)
