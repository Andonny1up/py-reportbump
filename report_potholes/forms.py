from django import forms
from .models import Pothole

class PotholeForm(forms.ModelForm):
    class Meta:
        model = Pothole
        fields = ['reported_by','phone','photo', 'location',]