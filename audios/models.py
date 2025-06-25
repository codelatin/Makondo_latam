from django.db import models
from cloudinary.models import CloudinaryField
from django.utils import timezone

# Create your models here.
class Audio(models.Model):
    titulo = models.CharField(max_length=200)
    interprete = models.CharField(max_length=200)
    compositor = models.CharField(max_length=200)
    genero = models.CharField(max_length=100)
    derechos_autor = models.CharField(max_length=100, null=True, blank=True)
    
    imagen = CloudinaryField('image') 
    archivo = CloudinaryField(resource_type='video')
    fecha_creacion = models.DateTimeField(default=timezone.now)
    fecha_actualizacion = models.DateTimeField(auto_now=True)
    
    class Meta:
        db_table = 'audios'
        ordering = ['-fecha_creacion']
    
    def __str__(self):
        return f"{self.titulo} - {self.interprete}"
    
    def total_reproducciones(self):
        return self.reproducciones.count()
 


class ReproduccionAudio(models.Model):
    audio = models.ForeignKey('Audio', on_delete=models.CASCADE, related_name='reproducciones')
    user = models.ForeignKey('auths.Auth', on_delete=models.CASCADE, null=True, blank=True)  # Referencia directa
    timestamp = models.DateTimeField(auto_now_add=True)
    direccion_ip = models.GenericIPAddressField(null=True, blank=True)
    duracion_escuchada = models.DurationField(null=True, blank=True)
    completo = models.BooleanField(default=False)
    
    class Meta:
        db_table = 'audio_reproducciones'
        verbose_name = "Reproducción"
        verbose_name_plural = "Reproducciones"
        ordering = ['-timestamp']

    def __str__(self):
        return f"Reproducción de {self.audio.titulo}"



class ContactoDescarga(models.Model):
    nombre = models.CharField(max_length=100)
    correo = models.EmailField()
    telefono = models.CharField(max_length=20)
    fecha_descarga = models.DateTimeField(auto_now_add=True)
    ip_address = models.GenericIPAddressField(null=True, blank=True)
    
    audio = models.ForeignKey(
        Audio,
        on_delete=models.SET_NULL,
        null=True,
        blank=True,
        verbose_name="Audio Descargado"
    )

    def __str__(self):
        return f"{self.nombre} - {self.audio.titulo if self.audio else 'Sin audio'}"

    class Meta:
        verbose_name = "Registro de Descarga"
        verbose_name_plural = "Registros de Descargas"
        ordering = ['-fecha_descarga']



