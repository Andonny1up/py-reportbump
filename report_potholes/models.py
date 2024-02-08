from django.db import models

# Create your models here.
class Pothole(models.Model):
    reported_by = models.CharField('reportado por',max_length=255, null=True, blank=True)
    phone = models.CharField('teléfono',max_length=15, null=True, blank=True)
    approved = models.BooleanField('aprobado',default=False)
    photo = models.ImageField('foto',upload_to='potholes/')
    latitude = models.DecimalField(max_digits=9, decimal_places=6, null=True, blank=True)
    longitude = models.DecimalField(max_digits=9, decimal_places=6, null=True, blank=True)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)