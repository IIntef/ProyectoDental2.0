from django.urls import path
from . import views
from django.contrib.auth import views as auth_views


urlpatterns = [
    path('crear-historias/', views.crearhistorias, name="crearhistorias"),
    path('ver-historias/<int:id>', views.verhistorias, name="verhistorias"),
    path('list-historias/', views.listhistorias, name="listhistorias"),
    path('eliminarhistorias/<int:id>/', views.eliminarhistorias, name="eliminarhistorias"),
]