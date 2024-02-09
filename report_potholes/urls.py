from django.urls import path, include
from . import views

app_name = 'report_potholes'

urlpatterns = [
    # admin potholes
    path('solicitude', views.UnapprovedPotholeListView.as_view(), name='solicitude_potholes'),
    path('approve_pothole/<int:pk>/', views.approve_pothole, name='approve_pothole'),
]
