from django.shortcuts import render,get_object_or_404, redirect
from django.urls import reverse_lazy
from django.views.generic import ListView, TemplateView
from django.views.generic.edit import CreateView
from .models import Pothole
from .forms import PotholeForm
from django.core.serializers.json import DjangoJSONEncoder
import json
# Create your views here.

class PotholeCreateView(CreateView):
    model = Pothole
    form_class = PotholeForm
    template_name = 'report_potholes/pothole_add.html'
    # success_url = '/report_potholes/thanks/'
    success_url = reverse_lazy('index')
    

class UnapprovedPotholeListView(ListView):
    model = Pothole
    template_name = 'report_potholes/pothole_solicitude.html'  # reemplaza con el nombre de tu plantilla
    context_object_name = 'potholes'
    paginate_by = 10

    def get_queryset(self):
        return Pothole.objects.filter(approved=False)
    

def approve_pothole(request, pk):
    pothole = get_object_or_404(Pothole, pk=pk)
    pothole.approved = True
    pothole.save()
    return redirect('solicitude_potholes')


class ApprovedPotholeMapView(TemplateView):
    template_name = 'report_potholes/pothole_maps.html'  # reemplaza con el nombre de tu plantilla

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        potholes = Pothole.objects.filter(approved=True).values('latitude', 'longitude')
        context['potholes'] = json.dumps(list(potholes), cls=DjangoJSONEncoder, ensure_ascii=False)
        # context['potholes'] = Pothole.objects.filter(approved=True)
        return context