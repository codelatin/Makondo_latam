from django.db import models
from cloudinary.models import CloudinaryField

# Create your models here.

class Audio(models.Model):
    titulo = models.CharField(max_length=200)
    interprete = models.CharField(max_length=200)
    compositor = models.CharField(max_length=200)
    genero = models.CharField(max_length=100)
    derechos_autor = models.CharField(max_length=100, null=True, blank=True)
    
    imagen = CloudinaryField('image') 
    archivo = CloudinaryField(resource_type='video')
    def __str__(self):
        return self.titulo

