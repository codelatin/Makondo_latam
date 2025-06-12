from django.urls import path, include
from . import views

app_name= 'audios'

urlpatterns = [
    # Vista web - inicio
    path('', views.inicio, name='inicio'),


]
