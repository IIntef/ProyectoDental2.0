from django.urls import path
from . import views
from django.contrib.auth import views as auth_views

urlpatterns = [
    path('', views.inicio, name='inicio'),
    path('base/', views.base, name="base"),
    path('dashboardDoc/', views.dashboardDoc, name="dashboardDoc"),
    path('loginregister/', views.registrarme, name="loginregister"),
    path('dashboard/', views.dashboard, name="dashboard"),
    path('signout/', views.signout, name="signout"),
    path('configuracion/<int:id>/', views.configuracion, name="configuracion"),
    path('correo/', views.correo, name="correo"),
    path('calendario/', views.calendario, name="calendario"),
    
    path('crear-citas/', views.crearcitas, name="crearcitas"),
    path('editar-citas/<int:id>', views.editarcitas, name="editarcitas"),
    path('list-citas/', views.listcitas, name="listcitas"),
    
    path('crear-cuentas/', views.crearcuentas, name="crearcuentas"),
    path('editar-cuentas/<int:id>', views.editarcuentas, name="editarcuentas"),
    path('list-cuentas/', views.listcuentas, name="listcuentas"),
    
    path('crear-fechas/', views.crearfechas, name="crearfechas"),
    path('editar-fechas/', views.editarfechas, name="editarfechas"),
    path('list-fechas/', views.listfechas, name="listfechas"),
    
    path('crear-historias/', views.crearhistorias, name="crearhistorias"),
    path('ver-historias/<int:id>', views.verhistorias, name="verhistorias"),
    path('list-historias/', views.listhistorias, name="listhistorias"),
    path('eliminarhistorias/<int:id>/', views.eliminarhistorias, name="eliminarhistorias"),

    
    path('crear-elemento/', views.crearelemento, name="crearelemento"),
    path('editar-elemento/', views.editarelemento, name="editarelemento"),
    path('list-elemento/', views.listelemento, name="listelemento"),
    
    path('fetch-user-details/', views.fetch_user_details, name='fetch_user_details'),
    path('forgot-password/', views.forgot_password, name='forgot_password'),
    path('reset/<uidb64>/<token>/', auth_views.PasswordResetConfirmView.as_view(), name='password_reset_confirm'),
    path('reset/done/', auth_views.PasswordResetCompleteView.as_view(), name='password_reset_complete'),
]