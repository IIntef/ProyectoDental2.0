from django import forms
from .models import UserProfile, Valoracion

class UserForm(forms.ModelForm):
    class Meta:
        model = UserProfile
        fields = ['tipo', 'numero', 'username', 'imagen', 'email', 'direccion', 'edad', 'ocupacion', 'celular', 'acudiente']
        
    tipo = forms.ChoiceField(choices=UserProfile.TIPO_CHOICES)
class ValoracionForm(forms.ModelForm):
    class Meta:
        model = Valoracion
        exclude = ['user', 'username', 'numero']
        widgets = {
            'fecha_historia': forms.DateInput(attrs={'type': 'date'}), 
        }

