from django.contrib.auth.decorators import login_required, user_passes_test
from django.shortcuts import render, redirect, get_object_or_404

from inicio.forms import InventarioForm
from inicio.models import Inventario
import inicio.views as traer

@login_required
@user_passes_test(traer.es_superusuario, login_url='acceso_denegado')
def eliminarelementos(request, id):
    elementoseliminar = get_object_or_404(Inventario, id=id)
    
    if request.method == 'POST':
        elementoseliminar.delete()
        return redirect('listelementos')
    
    return redirect('listelementos')

@login_required
@user_passes_test(traer.es_superusuario, login_url='acceso_denegado')
def crearelementos(request):
    if request.method == 'POST':
        form = InventarioForm(request.POST, request.FILES)
        if form.is_valid():
            form.save()
            return redirect('listelementos')  
    else:
        form = InventarioForm()
    
    return render(request, 'crearelementos.html', {'form': form})

@login_required
@user_passes_test(traer.es_superusuario, login_url='acceso_denegado')
def listelementos(request):
    inventarios = Inventario.objects.all()
    return render(request, 'listelementos.html', {'inventarios': inventarios})

@login_required
@user_passes_test(traer.es_superusuario, login_url='acceso_denegado')
def editarelementos(request, id):
    form_edelem = Inventario.objects.get(id=id)
    if request.method == 'POST':
        form = InventarioForm(request.POST, request.FILES, instance=form_edelem)
        if form.is_valid():
            form.save()
            return redirect('listelementos') 
    else:
        form = InventarioForm(instance=form_edelem)
    return render(request, 'editarelementos.html', {'form': form})