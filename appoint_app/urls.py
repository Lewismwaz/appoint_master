from django.urls import path
from . import views
from account.views import appointment_pdf

urlpatterns = [
    path("", views.dashboard, name='dashboard'),
    path("appointment_pdf/", appointment_pdf, name='appointment_pdf'),
    path("home/", views.home, name='home'), 
    path('terms/', views.terms, name='terms'),
]
