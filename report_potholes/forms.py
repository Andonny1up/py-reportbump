from django import forms
from .models import Pothole

class PotholeForm(forms.ModelForm):
    class Meta:
        model = Pothole
        fields = ['reported_by', 'phone', 'photo', 'latitude', 'longitude']
        labels = {
            'reported_by': 'Reportado por',
            'phone': 'Teléfono',
            'photo': 'Foto',
            'latitude': 'Latitud',
            'longitude': 'Longitud',
        }
        widgets = {
            'reported_by': forms.TextInput(attrs={'class': 'form-control'}),
            'phone': forms.TextInput(attrs={'class': 'form-control'}),
            'photo': forms.FileInput(attrs={'class': 'form-control-file'}),
            'latitude': forms.NumberInput(attrs={'class': 'form-control'}),
            'longitude': forms.NumberInput(attrs={'class': 'form-control'}),
        }