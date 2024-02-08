from django.shortcuts import render
from django.urls import reverse_lazy
from django.views.generic.edit import CreateView
from .models import Pothole
from .forms import PotholeForm
# Create your views here.

class PotholeCreateView(CreateView):
    model = Pothole
    form_class = PotholeForm
    template_name = 'report_potholes/pothole_add.html'
    success_url = '/report_potholes/thanks/'
    # success_url = reverse_lazy('nombre_de_tu_url')