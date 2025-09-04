from django import forms
from django.contrib.auth.forms import UserCreationForm
from django.contrib.auth.models import User
from .models import Client

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
