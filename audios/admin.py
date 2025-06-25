from django.contrib import admin

# Register your models here.
from .models import Audio, ReproduccionAudio,ContactoDescarga

class AudioAdmin(admin.ModelAdmin):
    list_display = ('titulo', 'genero', 'compositor', 'interprete')  # Campos visibles en la lista
    search_fields = ('titulo', 'genero', 'compositor', 'interprete')  # Campos que se pueden buscar

admin.site.register(Audio, AudioAdmin)
admin.site.register(ReproduccionAudio)

@admin.register(ContactoDescarga)
class ContactoDescargaAdmin(admin.ModelAdmin):
    list_display = ('nombre', 'correo', 'telefono', 'audio', 'fecha_descarga', 'ip_address')
    list_filter = ('fecha_descarga', 'audio')
    search_fields = ('nombre', 'correo', 'telefono', 'audio')
    readonly_fields = ('fecha_descarga', 'ip_address')
    ordering = ('-fecha_descarga',)
    
    fieldsets = (
        ('Información de Contacto', {
            'fields': ('nombre', 'correo', 'telefono')
        }),
        ('Información de Descarga', {
            'fields': ( 'audio', 'fecha_descarga', 'ip_address')
        }),
    )
    #listo desarrolladores mision completed un saludo!