from django import forms
from .models import UserProfile, Valoracion

class UserForm(forms.ModelForm):
    class Meta:
        model = UserProfile
        fields = '__all__'

class ValoracionForm(forms.ModelForm):
    class Meta:
        model = Valoracion
        fields = '__all__'
