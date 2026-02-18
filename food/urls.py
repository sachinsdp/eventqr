from django.urls import path
from . import views

urlpatterns = [
    path('', views.generate_qr, name="generate_qr"),
    path('scanner/', views.scanner_page, name="scanner"),
    path('verify/', views.verify_scan, name="verify_scan"),
    path('dashboard/', views.dashboard, name="dashboard"),

]
