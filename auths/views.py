from django.shortcuts import render

# Create your views here.
def registro(request):
    return render(request, 'cuentas/registro.html')

def login(request):
    return render(request, 'cuentas/login.html')

def logout(request):
    return render(request, 'cuentas/logout.html')