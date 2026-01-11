"""config URL Configuration

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/4.1/topics/http/urls/
Examples:
Function views
    1. Add an import:  from my_app import views
    2. Add a URL to urlpatterns:  path('', views.home, name='home')
Class-based views
    1. Add an import:  from other_app.views import Home
    2. Add a URL to urlpatterns:  path('', Home.as_view(), name='home')
Including another URLconf
    1. Import the include() function: from django.urls import include, path
    2. Add a URL to urlpatterns:  path('blog/', include('blog.urls'))
"""
from django.contrib import admin
from django.urls import path, include
from django.conf import settings
from django.conf.urls.static import static
from users import views  # Importar les vistes de l'app users

# Definició dels patrons d'URL principals del projecte
urlpatterns = [
    # URL per accedir a l'administració de Django
    path('admin/', admin.site.urls),
    
    # Incloure totes les URLs de l'app users amb el prefix 'users/'
    path('users/', include('users.urls')),
    
    path('events/', include('events.urls')),
    path('chat/', include('chat.urls')),
    
    # URL per a la pàgina principal (arrel del lloc)
    path('', views.home_view, name='home'),
]

# Això permet accedir a imatges pujades pels usuaris (com avatars) en mode DEBUG
if settings.DEBUG:
    urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)