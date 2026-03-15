from django.urls import path
from . import views

urlpatterns = [
    path('', views.generate_qr, name="generate_qr"),
    path('scanner/', views.scanner_page, name="scanner"),
    path('verify/', views.verify_scan, name="verify_scan"),
    path('dashboard/', views.dashboard, name="dashboard"),
    path("panel/<int:panel_id>/", views.submit_question, name="submit_question"),
    path("moderator/", views.moderator_view, name="moderator_view"),
]



