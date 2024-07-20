from django.urls import path
from . import views
from django.contrib.auth import views as auth_views


urlpatterns = [ 
    path('crear-citas/', views.crearcitas, name="crearcitas"),
    path('editar-citas/<int:cita_id>', views.editarcitas, name="editarcitas"),
    path('list-citas/', views.listcitas, name="listcitas"),
    path('cancelar-cita/<int:cita_id>/', views.cancelar_cita, name='cancelar_cita'),
    path('confirmar-actualizacion/<int:cita_id>/', views.confirmar_actualizacion_cita, name='confirmar_actualizacion_cita'),
    path('get-horas-disponibles/', views.get_horas_disponibles, name='get_horas_disponibles'),
]