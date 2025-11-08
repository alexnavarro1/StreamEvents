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
    
    # Camp de contrasenya 1 - definit manualment (no està al model)
    password1 = forms.CharField(
        label='Contrasenya',
        widget=forms.PasswordInput(attrs={
            'class': 'form-control',
            'placeholder': 'Contrasenya'
        }),
        help_text='La contrasenya ha de tenir almenys 8 caràcters.'
    )
    
    # Camp de confirmació de contrasenya - també definit manualment
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
        # Configuració dels widgets per a cada camp amb classes Bootstrap
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
        # Etiquetes personalitzades per als camps
        labels = {
            'username': 'Nom d\'usuari',
            'email': 'Correu electrònic',
            'first_name': 'Nom',
            'last_name': 'Cognom',
        }

    def clean_username(self):
        """Validació personalitzada per al nom d'usuari"""
        username = self.cleaned_data.get('username')
        
        # Validar format username amb expressió regular
        if not re.match(r'^[\w.@+-]+$', username):
            raise ValidationError(
                'El nom d\'usuari només pot contenir lletres, números i els caràcters @/./+/-/_'
            )
        
        # Validar que no comenci per número
        if username[0].isdigit():
            raise ValidationError('El nom d\'usuari no pot començar per número')
            
        return username

    def clean_email(self):
        """Validació personalitzada per l'email"""
        email = self.cleaned_data.get('email')
        
        # Comprovar que l'email no estigui ja registrat
        if email and CustomUser.objects.filter(email=email).exists():
            raise ValidationError('Aquest email ja està registrat.')
            
        return email

    def clean_password2(self):
        """Validació personalitzada per la confirmació de contrasenya"""
        password1 = self.cleaned_data.get('password1')
        password2 = self.cleaned_data.get('password2')
        
        # Comprovar que les dues contrasenyes coincideixen
        if password1 and password2 and password1 != password2:
            raise ValidationError('Les contrasenyes no coincideixen.')
            
        # Validar complexitat de la contrasenya amb els validadors de Django
        if password1:
            validate_password(password1)
            
        return password2

    def save(self, commit=True):
        """Mètode per guardar l'usuari amb la contrasenya encriptada"""
        # Cridar el mètode save del pare sense guardar encara
        user = super().save(commit=False)
        
        # Establir la contrasenya encriptada
        user.set_password(self.cleaned_data['password1'])
        
        # Guardar a la base de dades si commit és True
        if commit:
            user.save()
            
        return user

class CustomUserUpdateForm(forms.ModelForm):
    """Formulari per editar perfil d'usuari existent"""
    
    class Meta:
        model = CustomUser
        fields = ['first_name', 'last_name', 'display_name', 'bio', 'avatar']
        # Configuració dels widgets per a l'edició de perfil
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
        # Etiquetes personalitzades per als camps d'edició
        labels = {
            'first_name': 'Nom',
            'last_name': 'Cognom',
            'display_name': 'Nom a mostrar',
            'bio': 'Biografia',
            'avatar': 'Avatar',
        }

class CustomAuthenticationForm(AuthenticationForm):
    """Formulari de login que permet email o username"""
    
    # Redefinir el camp username per acceptar tant email com username
    username = forms.CharField(
        label='Email o Nom d\'usuari',
        widget=forms.TextInput(attrs={
            'class': 'form-control',
            'placeholder': 'Email o nom d\'usuari'
        })
    )

    def clean(self):
        """Validació personalitzada per l'autenticació"""
        username = self.cleaned_data.get('username')
        password = self.cleaned_data.get('password')

        if username and password:
            # Variable per emmagatzemar l'usuari autenticat
            user = None
            
            # Provar si l'entrada és un email vàlid
            try:
                validate_email(username)
                # Si és un email vàlid, buscar l'usuari per email
                try:
                    user_obj = CustomUser.objects.get(email=username)
                    # Intentar autenticar amb el username trobat
                    user = authenticate(
                        request=self.request,
                        username=user_obj.username,
                        password=password
                    )
                except CustomUser.DoesNotExist:
                    # Si no es troba l'usuari amb aquest email, passar a la següent prova
                    pass
            except ValidationError:
                # Si no és un email vàlid, provar d'autenticar directament com a username
                user = authenticate(
                    request=self.request,
                    username=username,
                    password=password
                )

            # Si no s'ha trobat cap usuari vàlid, llançar error
            if user is None:
                raise ValidationError(
                    'Credencials incorrectes. Verifica el teu email/usuari i contrasenya.'
                )
                
            # Emmagatzemar l'usuari a les dades netejades
            self.cleaned_data['user'] = user
            
        return self.cleaned_data