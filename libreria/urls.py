from django.urls import path
from . import views
from django.conf import settings
from django.contrib.staticfiles.urls import static

urlpatterns = [
    path('start/', views.start, name="start"),
    path('nosotros/', views.nosotros, name="nosotros"),
    path('libros/', views.libros, name="libros"),
    path('crear/', views.crear, name="crear"),
    path('editar/<int:id>', views.editar, name="editar"),
    path('eliminar/<int:id>', views.eliminar, name="eliminar"),
    path('categorias/', views.categorias, name="categorias"),
    path('crear_cat/', views.crear_cat, name="crear_cat"),
    path('editar_cat/<int:id>', views.editar_cat, name="editar_cat"),
    path('eliminar_cat/<int:id>', views.eliminar_cat, name="eliminar_cat"),
    path('accounts/logout/', views.custom_logout, name='logout'),
] + static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)

