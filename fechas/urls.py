from django.urls import path
from . import views
from django.contrib.auth import views as auth_views


urlpatterns = [
    path('crear-fechas/', views.crearfechas, name="crearfechas"),
    path('editar-fechas/<int:id>', views.editarfechas, name="editarfechas"),
    path('list-fechas/', views.listfechas, name="listfechas"),
    path('eliminarfechas/<int:id>/', views.eliminarfechas, name="eliminarfechas"),
]