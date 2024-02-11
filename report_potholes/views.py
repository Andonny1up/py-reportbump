from django.contrib.auth.mixins import LoginRequiredMixin, PermissionRequiredMixin
from django.contrib.auth.decorators import login_required
from django.shortcuts import render,get_object_or_404, redirect
from django.urls import reverse_lazy, reverse
from django.views.generic import ListView, TemplateView, DetailView, DeleteView
from django.views.generic.edit import CreateView
from .models import Pothole
from .forms import PotholeForm
from django.core.serializers.json import DjangoJSONEncoder
from django.core import serializers
from django.core.exceptions import PermissionDenied
import json
from django.conf import settings
import os
# Create your views here.

class PotholeCreateView(CreateView):
    """Vista para reportar un bache."""
    model = Pothole
    form_class = PotholeForm
    template_name = 'report_potholes/pothole_add.html'
    # success_url = '/report_potholes/thanks/'
    success_url = reverse_lazy('thanks')
    

class PotholeThanksView(TemplateView):
    """vista de agradecimiento."""
    template_name = 'report_potholes/pothole_thanks.html'


class ApprovedPotholeMapView(TemplateView):
    """Muestra un mapa con los baches aprobados."""
    template_name = 'report_potholes/pothole_maps.html'  # reemplaza con el nombre de tu plantilla

    def get_context_data(self, **kwargs):
        # context = super().get_context_data(**kwargs)
        # potholes = Pothole.objects.filter(approved=True).values('latitude', 'longitude')
        # context['potholes'] = json.dumps(list(potholes), cls=DjangoJSONEncoder, ensure_ascii=False)
        # # context['potholes'] = Pothole.objects.filter(approved=True)
        # return context
    
        context = super().get_context_data(**kwargs)
        potholes = Pothole.objects.filter(approved=True)
        potholes_data = []
        for pothole in potholes:
            pothole_data = {
                'latitude': pothole.latitude,
                'longitude': pothole.longitude,
                'url': reverse('pothole_detail', args=[pothole.id])
            }
            potholes_data.append(pothole_data)
        context['potholes'] = json.dumps(potholes_data, cls=DjangoJSONEncoder, ensure_ascii=False)
        context['total_potholes'] = potholes.count()
        return context
    

class PotholeDetailView(DetailView):
    """Muestra los detalles de un bache."""
    model = Pothole
    template_name = 'report_potholes/pothole_detail.html'
    context_object_name = 'pothole'


# administrador
class UnapprovedPotholeListView(LoginRequiredMixin, PermissionRequiredMixin, ListView):
    """Muestra los baches no aprobados."""
    model = Pothole
    template_name = 'report_potholes/potholes/pothole_solicitude.html'  # reemplaza con el nombre de tu plantilla
    context_object_name = 'potholes'
    paginate_by = 10
    permission_required = 'report_potholes.view_pothole'

    def get_queryset(self):
        return Pothole.objects.filter(approved=False)


@login_required
def approve_pothole(request, pk):
    """Aprueba un bache."""
    if not request.user.has_perm('app_name.can_approve_pothole'):
        raise PermissionDenied
    pothole = get_object_or_404(Pothole, pk=pk)
    pothole.approved = True
    pothole.save()
    return redirect('admin_ssu:report_potholes:solicitude_potholes')
    

class PotholeDeleteView(LoginRequiredMixin, PermissionRequiredMixin, DeleteView):
    """Vista para descartar y eliminar un bache."""
    model = Pothole
    success_url = reverse_lazy('admin_ssu:report_potholes:solicitude_potholes')
    permission_required = 'report_potholes.delete_pothole'

    # def delete(self, request, *args, **kwargs):
    #     pothole = self.get_object()
    #     # Borra el archivo de imagen del sistema de archivos
    #     if pothole.photo:
    #         if os.path.isfile(os.path.join(settings.MEDIA_ROOT, pothole.photo.path)):
    #             print(settings.MEDIA_ROOT, pothole.photo.path)
    #             os.remove(os.path.join(settings.MEDIA_ROOT, pothole.photo.path))
    #     # Llama al método delete original para eliminar el objeto en la base de datos
    #     return super().delete(request, *args, **kwargs)

class ApprovedPotholesListView(LoginRequiredMixin, PermissionRequiredMixin, ListView):
    model = Pothole
    template_name = 'report_potholes/potholes/potholes_list.html'
    context_object_name = 'potholes'
    paginate_by = 10
    permission_required = 'report_potholes.view_pothole'

    def get_queryset(self):
        return Pothole.objects.filter(approved=True)
    

from math import radians, sin, cos, sqrt, atan2

class PotholeDetailMapView(DetailView):
    model = Pothole
    template_name = 'report_potholes/potholes/pothole_detail.html'
    context_object_name = 'pothole'

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)

        # Radio de la Tierra en kilómetros
        R = 6371.0

        lat1 = radians(self.object.latitude)
        lon1 = radians(self.object.longitude)

        nearby_potholes = []
        for pothole in Pothole.objects.filter(approved=True):
            lat2 = radians(pothole.latitude)
            lon2 = radians(pothole.longitude)

            dlon = lon2 - lon1
            dlat = lat2 - lat1

            a = sin(dlat / 2)**2 + cos(lat1) * cos(lat2) * sin(dlon / 2)**2
            c = 2 * atan2(sqrt(a), sqrt(1 - a))

            distance = R * c

            # Si la distancia es menor a 1 kilómetro, añade el bache a la lista
            if distance < 1:
                nearby_potholes.append({'latitude': float(pothole.latitude), 'longitude': float(pothole.longitude),'url': reverse('pothole_detail', args=[pothole.id])})

        context['potholejs'] = {'latitude': float(self.object.latitude), 'longitude': float(self.object.longitude)}
        context['nearby_potholes'] = nearby_potholes
        return context