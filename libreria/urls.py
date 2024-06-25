from django.urls import path
from . import views

urlpatterns = [
    path('nosotros/', views.nosotros, name="nosotros"),
    path('libros/', views.libros, name="libros"),
    path('start/', views.start, name="start"),
    path('crear/', views.crear, name="crear"),
]