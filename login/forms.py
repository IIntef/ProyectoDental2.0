from django import forms
from .models import UserProfile, Valoracion

class UserForm(forms.ModelForm):
    class Meta:
        model = UserProfile
        fields = ['tipo', 'numero', 'username', 'email', 'direccion', 'edad', 'ocupacion', 'celular', 'acudiente']
        
class ValoracionForm(forms.ModelForm):
    class Meta:
        model = Valoracion
        exclude = ['user', 'username', 'numero']
        widgets = {
            'fecha_historia': forms.DateInput(attrs={'type': 'date'}), 
        }
