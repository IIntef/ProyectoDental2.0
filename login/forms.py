from django import forms
from .models import UserProfile, Valoracion, Inventario, Fecha, Cita
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

from django import forms
from .models import Cita, Fecha, UserProfile

from django import forms
from .models import Cita, Fecha, UserProfile

class CitaForm(forms.ModelForm):
    fecha = forms.DateField(widget=forms.DateInput(attrs={'type': 'date'}))
    hora = forms.TimeField(widget=forms.TimeInput(attrs={'type': 'time'}))
    motivo = forms.ChoiceField(choices=Cita.MOTIVO_CHOICES)

    class Meta:
        model = Cita
        fields = ['fecha', 'hora', 'motivo', 'paciente']

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        if 'initial' in kwargs and kwargs['initial'].get('paciente') is None:
            self.fields.pop('paciente', None)
        else:
            self.fields['paciente'] = forms.ChoiceField(choices=self.get_pacientes_choices(), required=False)

    def get_pacientes_choices(self):
        pacientes = UserProfile.objects.filter(is_active=True)
        choices = [(perfil.numero, perfil.username) for perfil in pacientes]
        return choices

    def clean(self):
        cleaned_data = super().clean()
        paciente_numero = cleaned_data.get('paciente')

        # Verificar si se seleccionó un paciente
        if paciente_numero:
            try:
                paciente = UserProfile.objects.get(numero=paciente_numero, is_active=True)
                cleaned_data['paciente'] = paciente
            except UserProfile.DoesNotExist:
                self.add_error('paciente', 'El paciente seleccionado no existe o no está activo.')

        # Verificar si el paciente ya tiene una cita programada
        if 'paciente' in cleaned_data:
            paciente = cleaned_data['paciente']
            cita_existente = Cita.objects.filter(paciente=paciente, estado='programada').exists()
            if cita_existente:
                self.add_error('paciente', 'El paciente ya tiene una cita programada.')

        return cleaned_data

    def save(self, commit=True):
        cita = super().save(commit=False)
        fecha = self.cleaned_data['fecha']
        hora = self.cleaned_data['hora']
        fecha_hora, created = Fecha.objects.get_or_create(fecha=fecha, hora=hora)
        cita.fecha_hora = fecha_hora

        if 'paciente' in self.cleaned_data:
            cita.paciente = self.cleaned_data['paciente']

        if commit:
            cita.save()
        return cita


