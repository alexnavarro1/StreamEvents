from django import forms
from django.contrib.auth.forms import AuthenticationForm, UserCreationForm
from django.contrib.auth import authenticate
from django.core.exceptions import ValidationError
from django.core.validators import validate_email
from django.contrib.auth.password_validation import validate_password
from .models import CustomUser
import re

class CustomUserCreationForm(forms.ModelForm):
    """Formulari per registrar usuaris nous"""
    
    password1 = forms.CharField(
        label='Contrasenya',
        widget=forms.PasswordInput(attrs={
            'class': 'form-control',
            'placeholder': 'Contrasenya'
        }),
        help_text='La contrasenya ha de tenir almenys 8 caràcters.'
    )
    
    password2 = forms.CharField(
        label='Confirma la contrasenya',
        widget=forms.PasswordInput(attrs={
            'class': 'form-control',
            'placeholder': 'Confirma la contrasenya'
        }),
        help_text='Introdueix la mateixa contrasenya per verificació.'
    )

    class Meta:
        model = CustomUser
        fields = ['username', 'email', 'first_name', 'last_name']
        widgets = {
            'username': forms.TextInput(attrs={
                'class': 'form-control',
                'placeholder': 'Nom d\'usuari'
            }),
            'email': forms.EmailInput(attrs={
                'class': 'form-control',
                'placeholder': 'Correu electrònic'
            }),
            'first_name': forms.TextInput(attrs={
                'class': 'form-control',
                'placeholder': 'Nom'
            }),
            'last_name': forms.TextInput(attrs={
                'class': 'form-control',
                'placeholder': 'Cognom'
            }),
        }
        labels = {
            'username': 'Nom d\'usuari',
            'email': 'Correu electrònic',
            'first_name': 'Nom',
            'last_name': 'Cognom',
        }

    def clean_username(self):
        username = self.cleaned_data.get('username')
        
        if not re.match(r'^[\w.@+-]+$', username):
            raise ValidationError(
                'El nom d\'usuari només pot contenir lletres, números i els caràcters @/./+/-/_'
            )
        
        if username[0].isdigit():
            raise ValidationError('El nom d\'usuari no pot començar per número')
            
        return username

    def clean_email(self):
        email = self.cleaned_data.get('email')
        
        if email and CustomUser.objects.filter(email=email).exists():
            raise ValidationError('Aquest email ja està registrat.')
            
        return email

    def clean_password2(self):
        password1 = self.cleaned_data.get('password1')
        password2 = self.cleaned_data.get('password2')
        
        if password1 and password2 and password1 != password2:
            raise ValidationError('Les contrasenyes no coincideixen.')
            
        if password1:
            validate_password(password1)
            
        return password2

    def save(self, commit=True):
        user = super().save(commit=False)
        user.set_password(self.cleaned_data['password1'])
        
        if commit:
            user.save()
            
        return user

class CustomUserUpdateForm(forms.ModelForm):
    """Formulari per editar perfil d'usuari existent"""
    
    class Meta:
        model = CustomUser
        fields = ['first_name', 'last_name', 'display_name', 'bio', 'avatar']
        widgets = {
            'first_name': forms.TextInput(attrs={
                'class': 'form-control',
                'placeholder': 'Nom'
            }),
            'last_name': forms.TextInput(attrs={
                'class': 'form-control',
                'placeholder': 'Cognom'
            }),
            'display_name': forms.TextInput(attrs={
                'class': 'form-control',
                'placeholder': 'Nom a mostrar'
            }),
            'bio': forms.Textarea(attrs={
                'class': 'form-control',
                'rows': 4,
                'placeholder': 'Descriu-te...'
            }),
            'avatar': forms.FileInput(attrs={
                'class': 'form-control'
            })
        }
        labels = {
            'first_name': 'Nom',
            'last_name': 'Cognom',
            'display_name': 'Nom a mostrar',
            'bio': 'Biografia',
            'avatar': 'Avatar',
        }

class CustomAuthenticationForm(AuthenticationForm):
    """Formulari de login que permet email o username"""
    
    username = forms.CharField(
        label='Email o Nom d\'usuari',
        widget=forms.TextInput(attrs={
            'class': 'form-control',
            'placeholder': 'Email o nom d\'usuari'
        })
    )

    def clean(self):
        """Validació personalitzada per l'autenticació - VERSIÓ CORREGIDA"""
        username = self.cleaned_data.get('username')
        password = self.cleaned_data.get('password')

        if username is not None and password:
            # Intentar autenticar tant per email com per username
            user = None
            
            # Provar si és un email
            try:
                validate_email(username)
                # Si és un email vàlid, buscar per email
                try:
                    user_obj = CustomUser.objects.get(email=username)
                    user = authenticate(
                        request=self.request,
                        username=user_obj.username,
                        password=password
                    )
                except CustomUser.DoesNotExist:
                    # Si no existeix l'usuari amb aquest email, continuar
                    pass
            except ValidationError:
                # No és un email, provar per username
                user = authenticate(
                    request=self.request,
                    username=username,
                    password=password
                )

            if user is None:
                # Si no s'ha trobat cap usuari, llançar error
                raise forms.ValidationError(
                    'Credencials incorrectes. Verifica el teu email/usuari i contrasenya.'
                )
                
            # IMPORTANT: Establir self.user_cache per al mètode get_user()
            self.user_cache = user

        # Tornar les dades netejades
        return self.cleaned_data