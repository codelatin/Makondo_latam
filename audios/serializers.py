from rest_framework import serializers
from .models import Audio, ReproduccionAudio
from django.contrib.auth import get_user_model

User = get_user_model()

class AudioSerializer(serializers.ModelSerializer):
    class Meta:
        model = Audio
        fields = ['id', 'titulo', 'interprete', 'compositor', 'genero', 'derechos_autor', 'imagen', 'archivo']

class AudioStatsSerializer(serializers.ModelSerializer):
    total_reproducciones = serializers.IntegerField(read_only=True)
    reproducciones_mes = serializers.IntegerField(read_only=True)
    reproducciones_semana = serializers.IntegerField(read_only=True)
    
    class Meta:
        model = Audio
        fields = ['id', 'titulo', 'interprete', 'compositor', 'genero', 
                 'total_reproducciones', 'reproducciones_mes', 'reproducciones_semana']

class ReproduccionAudioSerializer(serializers.ModelSerializer):
    usuario_nombre = serializers.CharField(source='user.nombre', read_only=True)
    usuario_email = serializers.CharField(source='user.email', read_only=True)
    audio_titulo = serializers.CharField(source='audio.titulo', read_only=True)
    
    class Meta:
        model = ReproduccionAudio
        fields = ['id', 'audio', 'audio_titulo', 'user', 'usuario_nombre', 'usuario_email', 
                 'timestamp', 'direccion_ip', 'duracion_escuchada', 'completo']
        read_only_fields = ['timestamp']