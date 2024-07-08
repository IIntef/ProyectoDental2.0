from django.urls import path
from . import views

urlpatterns = [
    path('', views.inicio, name='inicio'),
    path('base/', views.base, name="base"),
    path('dashboardDoc/', views.dashboardDoc, name="dashboardDoc"),
    path('loginregister/', views.registrarme, name="loginregister"),
    path('dashboard/', views.dashboard, name="dashboard"),
    path('signout/', views.signout, name="signout"),
    path('configuracion/', views.configuracion, name="configuracion"),
    path('correo/', views.correo, name="correo"),
    path('calendario/', views.calendario, name="calendario"),
    
    path('crear-citas/', views.crearcitas, name="crearcitas"),
    path('editar-citas/', views.editarcitas, name="editarcitas"),
    path('list-citas/', views.listcitas, name="listcitas"),
    
    path('crear-cuentas/', views.crearcuentas, name="crearcuentas"),
    path('editar-cuentas/', views.editarcuentas, name="editarcuentas"),
    path('list-cuentas/', views.listcuentas, name="listcuentas"),
    
    path('crear-fechas/', views.crearfechas, name="crearfechas"),
    path('editar-fechas/', views.editarfechas, name="editarfechas"),
    path('list-fechas/', views.listfechas, name="listfechas"),
    
    path('crear-historias/', views.crearhistorias, name="crearhistorias"),
    path('editar-historias/', views.editarhistorias, name="editarhistorias"),
    path('list-historias/', views.listhistorias, name="listhistorias"),
    
    path('crear-elemento/', views.crearelemento, name="crearelemento"),
    path('editar-elemento/', views.editarelemento, name="editarelemento"),
    path('list-elemento/', views.listelemento, name="listelemento"),
]