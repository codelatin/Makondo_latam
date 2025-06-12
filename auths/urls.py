from django.urls import path
from . import views
app_name = 'auths' # saben? 

urlpatterns = [
    path('registro/', views.registro, name='registro'),
    path('login/', views.login, name='login'),
    path('logout/', views.logout, name='logout'),

]