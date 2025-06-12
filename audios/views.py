from django.shortcuts import render
from django.http import HttpResponse
from .models import Audio, ReproduccionAudio
from django.core.paginator import Paginator
from django.db.models import Q, Count
from django.utils import timezone
from datetime import timedelta
from .serializers import AudioSerializer
# Imports para Django REST Framework
from rest_framework import viewsets
from rest_framework.decorators import api_view, action
from rest_framework.response import Response
from .serializers import AudioStatsSerializer 
from auths.models import Auth 

# Create your views here.

def inicio(request): 
    # Aquí comienzo con la búsqueda Query
    query = request.GET.get('q', '')  # es una búsqueda sql, get: puedo enviar datos y los ve en la url de búsqueda y con post no 
    genero_filtro = request.GET.get('g', '')  # filtra cada género

    # Comenzamos con todos los audios
    lista_audios = Audio.objects.all()

    # aquí estoy filtrando por búsqueda de texto fíjense
    if query:
        lista_audios = lista_audios.filter(
            Q(titulo__icontains=query) |
            Q(genero__icontains=query)
        )

    # aquí filtro por el género seleccionado Desarrolladores
    if genero_filtro:
        lista_audios = lista_audios.filter(genero__iexact=genero_filtro)

    # realizo la Paginación
    paginator = Paginator(lista_audios, 20)
    page_number = request.GET.get('page')
    page_obj = paginator.get_page(page_number)

    # Construir URL absoluta para cada audio es (opcional) desarrolladores pero haganlo
    for audio in page_obj:
        audio.full_url = request.build_absolute_uri(audio.archivo.url)

    # Obtengo  todos los géneros únicos para el select mis amigos
    generos = Audio.objects.values_list('genero', flat=True).distinct().order_by('genero')

    return render(request, 'audios/inicio.html', {
        'audios': page_obj,
        'page_obj': page_obj,
        'is_paginated': page_obj.has_other_pages(),
        'q': query,
        'g': genero_filtro,  # Pasamos el filtro activo al template recuerdenlo
        'generos': generos   # Pasamos la lista de géneros amigos 
    })


class AudioStatsViewSet(viewsets.ReadOnlyModelViewSet):
    serializer_class = AudioStatsSerializer
    
    def get_queryset(self):
        now = timezone.now()
        mes_atras = now - timedelta(days=30)
        semana_atras = now - timedelta(days=7)
        
        return Audio.objects.annotate(
            total_reproducciones=Count('reproducciones'),
            reproducciones_mes=Count('reproducciones', 
                filter=Q(reproducciones__timestamp__gte=mes_atras)),
            reproducciones_semana=Count('reproducciones', 
                filter=Q(reproducciones__timestamp__gte=semana_atras))
        ).order_by('-total_reproducciones')

    @action(detail=False, methods=['get'])
    def mas_reproducidos(self, request):
        periodo = request.query_params.get('periodo', 'total')
        limit = int(request.query_params.get('limit', 10))
        
        if periodo == 'mes':
            order_field = '-reproducciones_mes'
        elif periodo == 'semana':
            order_field = '-reproducciones_semana'
        else:
            order_field = '-total_reproducciones'
            
        queryset = self.get_queryset().order_by(order_field)[:limit]
        serializer = self.get_serializer(queryset, many=True)
        return Response(serializer.data)


# View para registrar reproducciones
@api_view(['POST'])
def registrar_reproduccion(request):
    audio_id = request.data.get('audio_id')
    duracion_escuchada = request.data.get('duracion_escuchada')  #  Corregido:debne usar el nombre correcto del campo
    completo = request.data.get('completo', False)  # Corregido: es  el nombre correcto del campo del modelo
    
    try:
        audio = Audio.objects.get(id=audio_id)
        ReproduccionAudio.objects.create(
            audio=audio,
            user=request.user if request.user.is_authenticated else None,
            direccion_ip=request.META.get('REMOTE_ADDR'),  #  Corregido: usar el nombre correcto del campo
            duracion_escuchada=duracion_escuchada,  #  Corregido
            completo=completo  # Corregido
        )
        return Response({'status': 'success'})
    except Audio.DoesNotExist:
        return Response({'error': 'Audio no encontrado'}, status=404)
    except Exception as e:
        return Response({'error': str(e)}, status=500)  # aqui  Añado:el  manejo de errores general
'''
@api_view(['GET'])
def audio_list_api(request):
    audios = Audio.objects.all()
    serializer = AudioSerializer(audios, many=True)
    return Response(serializer.data)

@api_view(['GET'])
def audio_detail_api(request, pk):
    try:
        audio = Audio.objects.get(pk=pk)
        serializer = AudioSerializer(audio)
        return Response(serializer.data)
    except Audio.DoesNotExist:
        return Response({'error': 'Audio no encontrado'}, status=404)    
 '''
class AudioViewSet(viewsets.ReadOnlyModelViewSet):
    queryset = Audio.objects.all()
    serializer_class = AudioSerializer

