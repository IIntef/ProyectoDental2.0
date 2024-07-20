from django.urls import path
from . import views
from django.contrib.auth import views as auth_views


urlpatterns = [
    path('dashboard/', views.dashboard, name="dashboard"),
    path('signout/', views.signout, name="signout"),
    path('configuracion/<int:id>/', views.configuracion, name="configuracion"),
    path('correo/', views.correo, name="correo"),
    path('calendario/', views.calendario, name="calendario"),
]