from django.urls import path
from . import views
from django.contrib.auth import views as auth_views


urlpatterns = [
    path('', views.inicio, name='inicio'),
    path('base/', views.base, name="base"),
    path('loginregister/', views.registrarme, name="loginregister"),
    path('acceso-denegado/', views.acceso_denegado, name='acceso_denegado'),
    path('cuidados/', views.cuidados, name='cuidados'),
    path('about/', views.about, name='about'),
]