from django.urls import path, include
from . import views

app_name= 'audios'

urlpatterns = [
    # Vista web - inicio
    path('', views.inicio, name='inicio'),
    path('procesar-descarga/', views.procesar_descarga, name='procesar_descarga'),
    path('descargar-audio/<int:audio_id>/', views.descargar_audio, name='descargar_audio'),


]
