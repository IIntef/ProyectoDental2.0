from django import forms
from .models import UserProfile, Valoracion, Inventario, Fecha
from PIL import Image

class UserForm(forms.ModelForm):
    class Meta:
        model = UserProfile
        fields = ['tipo', 'numero', 'username', 'imagen', 'email', 'direccion', 'edad', 'ocupacion', 'celular', 'acudiente']

    tipo = forms.ChoiceField(choices=UserProfile.TIPO_CHOICES)

    def clean_imagen(self):
        imagen = self.cleaned_data.get('imagen')
        if imagen:
            try:
                # Abrir la imagen
                img = Image.open(imagen)
                # Verificar el formato
                if img.format.lower() not in ['jpeg', 'jpg', 'png', 'gif']:
                    raise forms.ValidationError("El formato de imagen no es soportado. Use JPEG, PNG o GIF.")
                # Verificar el tamaño (por ejemplo, menor a 5MB)
                if imagen.size > 5 * 1024 * 1024:
                    raise forms.ValidationError("La imagen es demasiado grande. El tamaño máximo es 5MB.")
                # Volver a colocar el puntero del archivo al inicio
                imagen.seek(0)
                return imagen
            except IOError:
                raise forms.ValidationError("No se pudo leer el archivo. Asegúrese de que es una imagen válida.")
        return imagen

class ValoracionForm(forms.ModelForm):
    class Meta:
        model = Valoracion
        exclude = ['user', 'username', 'numero']
        widgets = {
            'fecha_historia': forms.DateInput(attrs={'type': 'date'}), 
        }


class InventarioForm(forms.ModelForm):
    class Meta:
        model = Inventario
        fields = ['producto', 'cantidad', 'estado']

    estado = forms.ChoiceField(choices=Inventario.ESTADO)


class FechaForm(forms.ModelForm):
    class Meta:
        model = Fecha
        fields = ['fecha', 'hora']
        widgets = {
            'fecha': forms.DateInput(attrs={'type': 'date'}),
            'hora': forms.TimeInput(attrs={'type': 'time'}),
        }
