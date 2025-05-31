from django.shortcuts import render
from django.http import HttpResponse
from . models import Audio
from django.core.paginator import Paginator
from django.db.models import Q
# Create your views here.


""" 
def inicio(request):
    return render(request, 'audios/inicio.html')
"""
def inicio(request): 
#Aqui comienzo con la busqueda Query
    query = request.GET.get('q', '')# es una busqueda sql, get: puedo enviar datos y los ve en la url de busqueda y cxon post no 
    genero_filtro = request.GET.get('g', '')# filtra cada gewnero

    # Comenzamos con todos los audios
    lista_audios = Audio.objects.all()

    # aqui estoy filtrando  por búsqueda de texto fijeense
    if query:
        lista_audios = lista_audios.filter(
            Q(titulo__icontains=query) |
            Q(genero__icontains=query)
        )

    # aqui filtro por el  por género seleccionado
    if genero_filtro:
        lista_audios = lista_audios.filter(genero__iexact=genero_filtro)

    # realizo la  Paginación
    paginator = Paginator(lista_audios, 20)
    page_number = request.GET.get('page')
    page_obj = paginator.get_page(page_number)

    # Construir URL absoluta para cada audio (opcional)
    for audio in page_obj:
        audio.full_url = request.build_absolute_uri(audio.archivo.url)

    # Obtener todos los géneros únicos para el select
    generos = Audio.objects.values_list('genero', flat=True).distinct().order_by('genero')

    return render(request, 'audios/inicio.html', {
        'audios': page_obj,
        'page_obj': page_obj,
        'is_paginated': page_obj.has_other_pages(),
        'q': query,
        'g': genero_filtro,  # Pasamos el filtro activo al template
        'generos': generos   # Pasamos la lista de géneros
    })

   