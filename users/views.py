from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth import login, logout, authenticate
from django.contrib.auth.decorators import login_required
from django.contrib import messages
from django.urls import reverse
from .forms import CustomUserCreationForm, CustomUserUpdateForm, CustomAuthenticationForm
from .models import CustomUser

def register_view(request):
    """Vista de registre d'usuaris"""
    
    # Redirigir usuaris ja autenticats (evitar que usuari logejat accedeixi al registre)
    if request.user.is_authenticated:
        messages.info(request, 'Ja tens una sessió iniciada.')
        return redirect('users:profile')
    
    # Comprovar si s'ha enviat el formulari (mètode POST)
    if request.method == 'POST':
        # Crear formulari amb les dades enviades
        form = CustomUserCreationForm(request.POST)
        
        # Validar el formulari
        if form.is_valid():
            try:
                # Guardar l'usuari nou a la base de dades
                user = form.save()
                # Iniciar sessió automàticament després del registre
                login(request, user)
                
                # Missatge d'èxit per a l'usuari
                messages.success(
                    request,
                    f'Benvingut/da {user.first_name}! El teu compte s\'ha creat correctament.'
                )
                # Redirigir al perfil de l'usuari
                return redirect('users:profile')
                
            except Exception as e:
                # Manejar errors inesperats durant el registre
                messages.error(
                    request,
                    'Hi ha hagut un problema creant el compte. Torna-ho a provar.'
                )
        else:
            # El formulari conté errors de validació
            messages.error(
                request,
                'Hi ha errors en el formulari. Revisa les dades introduïdes.'
            )
    else:
        # Mostrar formulari buit (mètode GET)
        form = CustomUserCreationForm()
    
    # Renderitzar la plantilla de registre amb el formulari
    return render(request, 'registration/register.html', {
        'form': form,
        'title': 'Crear compte nou'
    })

def login_view(request):
    """Vista d'inici de sessió"""
    
    # Redirigir usuaris ja autenticats (evitar doble login)
    if request.user.is_authenticated:
        messages.info(request, 'Ja tens una sessió iniciada.')
        return redirect('users:profile')
    
    # Comprovar si s'ha enviat el formulari de login
    if request.method == 'POST':
        # Crear formulari d'autenticació amb les dades enviades
        form = CustomAuthenticationForm(request, data=request.POST)
        
        # Validar el formulari
        if form.is_valid():
            # Obtenir l'usuari autenticat
            user = form.get_user()
            # Iniciar sessió de l'usuari
            login(request, user)
            
            # Missatge de benvinguda
            messages.success(request, f'Benvingut/da de nou, {user.first_name}!')
            
            # Redirigir a la pàgina que intentava accedir o al perfil per defecte
            next_url = request.GET.get('next', 'users:profile')
            return redirect(next_url)
        else:
            # Credencials incorrectes
            messages.error(request, 'Email/usuari o contrasenya incorrectes.')
    else:
        # Mostrar formulari buit (mètode GET)
        form = CustomAuthenticationForm()
    
    # Renderitzar la plantilla de login amb el formulari
    return render(request, 'registration/login.html', {
        'form': form,
        'title': 'Iniciar sessió'
    })

def logout_view(request):
    """Vista de tancament de sessió"""
    # Comprovar si l'usuari està autenticat abans de fer logout
    if request.user.is_authenticated:
        # Tancar la sessió de l'usuari
        logout(request)
        # Missatge informatiu
        messages.info(request, 'Sessió tancada correctament.')
    
    # Redirigir a la pàgina principal
    return redirect('home')

@login_required  # Decorador que requereix que l'usuari estigui autenticat
def profile_view(request):
    """Vista del perfil de l'usuari autenticat"""
    # Renderitzar la plantilla del perfil amb les dades de l'usuari
    return render(request, 'users/profile.html', {
        'user': request.user,  # Passar l'objecte d'usuari a la plantilla
        'title': 'El meu perfil'
    })

@login_required  # Requereix autenticació per accedir a aquesta vista
def edit_profile_view(request):
    """Vista per editar el perfil"""
    
    # Comprovar si s'ha enviat el formulari d'edició
    if request.method == 'POST':
        # Crear formulari amb les dades i arxius (com l'avatar) enviats
        form = CustomUserUpdateForm(
            request.POST, 
            request.FILES,  # Important per pujar arxius com avatars
            instance=request.user  # Carregar les dades actuals de l'usuari
        )
        
        # Validar el formulari
        if form.is_valid():
            # Guardar els canvis al perfil
            form.save()
            # Missatge d'èxit
            messages.success(request, 'Perfil actualitzat correctament!')
            # Redirigir al perfil actualitzat
            return redirect('users:profile')
        else:
            # Hi ha errors en el formulari
            messages.error(request, 'Hi ha errors en el formulari.')
    else:
        # Mostrar formulari amb les dades actuals de l'usuari
        form = CustomUserUpdateForm(instance=request.user)
    
    # Renderitzar la plantilla d'edició de perfil
    return render(request, 'users/edit_profile.html', {
        'form': form,
        'title': 'Editar perfil'
    })

def public_profile_view(request, username):
    """Vista de perfil públic d'altres usuaris"""
    
    # Buscar l'usuari pel seu username, retornar 404 si no existeix
    user = get_object_or_404(CustomUser, username=username)
    
    # Renderitzar la plantilla de perfil públic
    return render(request, 'users/public_profile.html', {
        'profile_user': user,  # Passar l'objecte d'usuari del perfil públic
        'title': f'Perfil de {user.display_name or user.username}'  # Títol dinàmic
    })
    
def home_view(request):
    """Vista de la pàgina principal"""
    # Renderitzar la plantilla de la pàgina d'inici
    return render(request, 'home.html')