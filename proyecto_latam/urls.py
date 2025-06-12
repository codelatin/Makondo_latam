
"""
URL configuration for proyecto_latam project.

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/5.2/topics/http/urls/ 
Examples:
Function views
    1. Add an import: from my_app import views
    2. Add a URL to urlpatterns: path('', views.home, name='home')
Class-based views
    1. Add an import: from other_app.views import Home
    2. Add a URL to urlpatterns: path('', Home.as_view(), name='home')
Including another URLconf
    1. Import the include() function: from django.urls import include, path
    2. Add a URL to urlpatterns: path('blog/', include('blog.urls'))
"""

from django.contrib import admin
from django.urls import path, include
from audios.views import inicio, registrar_reproduccion  # Asegúrate de tener estas vistas
from rest_framework.routers import DefaultRouter
from audios.views import AudioViewSet, AudioStatsViewSet

# Configuración del router para la API REST
router = DefaultRouter()
router.register(r'audios', AudioViewSet, basename='audio')
router.register(r'audios/stats', AudioStatsViewSet, basename='audio-stats')

urlpatterns = [
    path('admin/', admin.site.urls),
    path('', include('home.urls')),  # Página de inicio/inicio.html

    # Ruta para la página web de audios
    path('audios/', include(('audios.urls', 'audios'), namespace='audios')),
    path('audios/reproduccion/', registrar_reproduccion, name='registrar_reproduccion'),
    path('auths/', include(('auths.urls', 'auths'), namespace='auths')),

    # Rutas para la API REST en /api/
    path('api/', include(router.urls)),
] #Excelente Desarolladores 










