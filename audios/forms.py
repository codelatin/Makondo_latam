# forms.py
from django import forms
from .models import ContactoDescarga
import re

class ContactoDescargaForm(forms.ModelForm):
    class Meta:
        model = ContactoDescarga
        fields = ['nombre', 'correo', 'telefono']
        widgets = {
            'nombre': forms.TextInput(attrs={
                'class': 'form-control',
                'placeholder': 'Tu nombre completo',
                'required': True
            }),
            'correo': forms.EmailInput(attrs={
                'class': 'form-control',
                'placeholder': 'tu@email.com',
                'required': True
            }),
            'telefono': forms.TextInput(attrs={
                'class': 'form-control',
                'placeholder': '+57 300 123 4567',
                'required': True
            }),
        }
        labels = {
            'nombre': 'Nombre completo',
            'correo': 'Correo electrónico',
            'telefono': 'Teléfono'
        }
    
    def clean_telefono(self):
        telefono = self.cleaned_data.get('telefono')
        if not telefono:
            raise forms.ValidationError("Este campo es obligatorio.")

        # Limpiar el número quitando todo lo que no sea dígito
        telefono_limpio = re.sub(r'\D', '', telefono)

        # Validar longitud mínima y máxima
        if not (10 <= len(telefono_limpio) <= 15):
            raise forms.ValidationError("El número debe tener entre 10 y 15 dígitos.")

        return telefono_limpio