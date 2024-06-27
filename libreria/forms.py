from django import forms
from .models import libro, Categoria

class LibroForm(forms.ModelForm):
    categoria = forms.ModelChoiceField(queryset=Categoria.objects.all())
    class Meta:
        model = libro
        fields = '__all__'
        
class CategoriaForm(forms.ModelForm):
    class Meta:
        model = Categoria
        fields = '__all__'