from django.urls import path
from . import views

urlpatterns = [
    path('admin/logout/', views.logout_view, name='logout'),
    path("", views.dashboard, name='dashboard'),
    path("home/", views.home, name='home'), 
    path('terms/', views.terms, name='terms'),
]
