from django.shortcuts import render
from .forms import FormularioRegistro
# Create your views here.
def registro(request): #funciones
    formulario= FormularioRegistro()
    context={
        'formulario':formulario
    }

    return render(request, 'cuentas/registro.html')

def login(request):
    return render(request, 'cuentas/login.html')

def logout(request):
    return render(request, 'cuentas/logout.html')