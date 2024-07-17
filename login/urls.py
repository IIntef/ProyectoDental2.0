from django.urls import path
from . import views
from django.contrib.auth import views as auth_views

urlpatterns = [
    path('', views.inicio, name='inicio'),
    path('base/', views.base, name="base"),
    path('loginregister/', views.registrarme, name="loginregister"),
    path('dashboard/', views.dashboard, name="dashboard"),
    path('signout/', views.signout, name="signout"),
    path('configuracion/<int:id>/', views.configuracion, name="configuracion"),
    path('correo/', views.correo, name="correo"),
    path('calendario/', views.calendario, name="calendario"),
    path('acceso-denegado/', views.acceso_denegado, name='acceso_denegado'),
    
    path('crear-citas/', views.crearcitas, name="crearcitas"),
    path('editar-citas/<int:cita_id>', views.editarcitas, name="editarcitas"),
    path('list-citas/', views.listcitas, name="listcitas"),
    path('cancelar-cita/<int:cita_id>/', views.cancelar_cita, name='cancelar_cita'),
    path('confirmar-actualizacion/<int:cita_id>/', views.confirmar_actualizacion_cita, name='confirmar_actualizacion_cita'),
    path('get-horas-disponibles/', views.get_horas_disponibles, name='get_horas_disponibles'),

    
    path('crear-cuentas/', views.crearcuentas, name="crearcuentas"),
    path('editar-cuentas/<int:id>', views.editarcuentas, name="editarcuentas"),
    path('list-cuentas/', views.listcuentas, name="listcuentas"),
    
    path('crear-fechas/', views.crearfechas, name="crearfechas"),
    path('editar-fechas/<int:id>', views.editarfechas, name="editarfechas"),
    path('list-fechas/', views.listfechas, name="listfechas"),
    path('eliminarfechas/<int:id>/', views.eliminarfechas, name="eliminarfechas"),
    path('horas-disponibles/', views.get_horas_disponibles, name='horas_disponibles'),

    
    path('crear-historias/', views.crearhistorias, name="crearhistorias"),
    path('ver-historias/<int:id>', views.verhistorias, name="verhistorias"),
    path('list-historias/', views.listhistorias, name="listhistorias"),
    path('eliminarhistorias/<int:id>/', views.eliminarhistorias, name="eliminarhistorias"),

    
    path('crear-elementos/', views.crearelementos, name="crearelementos"),
    path('editar-elementos/<int:id>', views.editarelementos, name="editarelementos"),
    path('list-elementos/', views.listelementos, name="listelementos"),
    path('eliminarelementos/<int:id>/', views.eliminarelementos, name="eliminarelementos"),
    
    path('fetch-user-details/', views.fetch_user_details, name='fetch_user_details'),


    path('password_reset/', auth_views.PasswordResetView.as_view(template_name='passwordreset/password_reset_form.html', email_template_name='passwordreset/password_reset_email.html'), name='password_reset'),
    path('password_reset_done/', auth_views.PasswordResetDoneView.as_view(template_name='passwordreset/password_reset_done.html'), name='password_reset_done'),
    path('password_reset_confirm/<uidb64>/<token>/', auth_views.PasswordResetConfirmView.as_view(template_name='passwordreset/password_reset_confirm.html'), name='password_reset_confirm'),
    path('password_reset_complete/', auth_views.PasswordResetCompleteView.as_view(template_name='passwordreset/password_reset_complete.html'), name='password_reset_complete'),

    path('cambiar-password/', views.cambiar_password, name='cambiar_password'),
]