from django.urls import path
from . import views

urlpatterns = [
    path('auth/', views.gmail_auth, name='gmail_auth'),
    path('oauth2callback2/', views.oauth2callback2, name='oauth2callback2'),
    path('inbox/', views.gmail_inbox, name='gmail_inbox'),
]