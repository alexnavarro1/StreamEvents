from django.urls import path
from . import views

# Namespace per a l'app d'usuaris - permet utilitzar 'users:' en les URL
app_name = 'users'

# Definició dels patrons d'URL per a l'app d'usuaris
urlpatterns = [
    # URL per al registre de nous usuaris
    path('register/', views.register_view, name='register'),
    
    # URL per a l'inici de sessió d'usuaris existents
    path('login/', views.login_view, name='login'),
    
    # URL per al tancament de sessió
    path('logout/', views.logout_view, name='logout'),
    
    # URL per visualitzar el perfil propi de l'usuari autenticat
    path('profile/', views.profile_view, name='profile'),
    
    # URL per editar el perfil de l'usuari autenticat
    path('profile/edit/', views.edit_profile_view, name='edit_profile'), 
    
    # URL per visualitzar el perfil públic d'altres usuaris (utilitza el username com a paràmetre)
    path('<str:username>/', views.public_profile_view, name='public_profile'),
]