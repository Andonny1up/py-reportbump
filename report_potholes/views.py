from django.contrib.auth.mixins import LoginRequiredMixin, PermissionRequiredMixin
from django.contrib.auth.decorators import login_required
from django.shortcuts import render,get_object_or_404, redirect
from django.urls import reverse_lazy
from django.views.generic import ListView, TemplateView, DeleteView
from django.views.generic.edit import CreateView
from .models import Pothole
from .forms import PotholeForm
from django.core.serializers.json import DjangoJSONEncoder
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
    success_url = reverse_lazy('index')
    

class UnapprovedPotholeListView(ListView, LoginRequiredMixin):
    """Muestra los baches no aprobados."""
    model = Pothole
    template_name = 'report_potholes/potholes/pothole_solicitude.html'  # reemplaza con el nombre de tu plantilla
    context_object_name = 'potholes'
    paginate_by = 10

    def get_queryset(self):
        return Pothole.objects.filter(approved=False)
    

@login_required
def approve_pothole(request, pk):
    """Aprueba un bache."""
    pothole = get_object_or_404(Pothole, pk=pk)
    pothole.approved = True
    pothole.save()
    return redirect('admin_ssu:report_potholes:solicitude_potholes')


class ApprovedPotholeMapView(TemplateView,LoginRequiredMixin):
    """Muestra un mapa con los baches aprobados."""
    template_name = 'report_potholes/pothole_maps.html'  # reemplaza con el nombre de tu plantilla

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        potholes = Pothole.objects.filter(approved=True).values('latitude', 'longitude')
        context['potholes'] = json.dumps(list(potholes), cls=DjangoJSONEncoder, ensure_ascii=False)
        # context['potholes'] = Pothole.objects.filter(approved=True)
        return context
    

class PotholeDeleteView(DeleteView,LoginRequiredMixin):
    """Vista para descartar y eliminar un bache."""
    model = Pothole
    success_url = reverse_lazy('admin_ssu:report_potholes:solicitude_potholes')

    # def delete(self, request, *args, **kwargs):
    #     pothole = self.get_object()
    #     # Borra el archivo de imagen del sistema de archivos
    #     if pothole.photo:
    #         if os.path.isfile(os.path.join(settings.MEDIA_ROOT, pothole.photo.path)):
    #             print(settings.MEDIA_ROOT, pothole.photo.path)
    #             os.remove(os.path.join(settings.MEDIA_ROOT, pothole.photo.path))
    #     # Llama al método delete original para eliminar el objeto en la base de datos
    #     return super().delete(request, *args, **kwargs)

class ApprovedPotholesListView(ListView, LoginRequiredMixin):
    model = Pothole
    template_name = 'report_potholes/potholes/potholes_list.html'
    context_object_name = 'potholes'
    paginate_by = 10

    def get_queryset(self):
        return Pothole.objects.filter(approved=True)