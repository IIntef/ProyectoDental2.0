from django.urls import path
from . import views
from django.contrib.auth import views as auth_views


urlpatterns = [
    path('crear-cuentas/', views.crearcuentas, name="crearcuentas"),
    path('editar-cuentas/<int:id>', views.editarcuentas, name="editarcuentas"),
    path('list-cuentas/', views.listcuentas, name="listcuentas"),
    path('cambiar-password/', views.cambiar_password, name='cambiar_password'),
    path('fetch-user-details/', views.fetch_user_details, name='fetch_user_details'),
]