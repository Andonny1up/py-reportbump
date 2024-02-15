from django.db import models
from imagekit.models import ImageSpecField
from imagekit.processors import ResizeToFill, ResizeToFit

# Create your models here.
class Pothole(models.Model):
    reported_by = models.CharField('reportado por',max_length=255, null=True, blank=True)
    phone = models.CharField('teléfono',max_length=15, null=True, blank=True)
    approved = models.BooleanField('aprobado',default=False)
    photo = models.ImageField('foto',upload_to='potholes/')
    thumbnail = ImageSpecField(source='photo',
                               processors=[ResizeToFit(300)],  # Cambia el tamaño de la imagen para que encaje en un cuadro de 800x800, manteniendo la relación de aspecto
                               format='JPEG',
                               options={'quality': 60})
    display_image = ImageSpecField(source='photo',
                                   processors=[ResizeToFit(800)],  # Para la imagen a mostrar en grande
                                   format='JPEG',
                                   options={'quality': 80})
    latitude = models.DecimalField(max_digits=9, decimal_places=7, null=True, blank=True)
    longitude = models.DecimalField(max_digits=9, decimal_places=7, null=True, blank=True)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)