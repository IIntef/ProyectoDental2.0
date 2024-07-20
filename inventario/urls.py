from django.urls import path
from . import views
from django.contrib.auth import views as auth_views


urlpatterns = [
    path('crear-elementos/', views.crearelementos, name="crearelementos"),
    path('editar-elementos/<int:id>', views.editarelementos, name="editarelementos"),
    path('list-elementos/', views.listelementos, name="listelementos"),
    path('eliminarelementos/<int:id>/', views.eliminarelementos, name="eliminarelementos"),
]