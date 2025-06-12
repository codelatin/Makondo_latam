from django.contrib import admin

# Register your models here.
from .models import Audio, ReproduccionAudio

class AudioAdmin(admin.ModelAdmin):
    list_display = ('titulo', 'genero', 'compositor', 'interprete')  # Campos visibles en la lista
    search_fields = ('titulo', 'genero', 'compositor', 'interprete')  # Campos que se pueden buscar

admin.site.register(Audio, AudioAdmin)
admin.site.register(ReproduccionAudio)