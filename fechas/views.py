from django.contrib.auth.decorators import login_required, user_passes_test
from django.shortcuts import render, redirect, get_object_or_404
from django.utils import timezone

from inicio.forms import FechaForm
from inicio.models import Fecha
import inicio.views as traer

@login_required
@user_passes_test(traer.es_superusuario, login_url='acceso_denegado')
def crearfechas(request):
    if request.method == 'POST':
        disponibilidad = FechaForm(request.POST)
        if disponibilidad.is_valid():
            disponibilidad.save()
            return redirect('listfechas')
    else:
        form = FechaForm()
    
    return render(request, 'crearfechas.html', {'form': form})

@login_required
@user_passes_test(traer.es_superusuario, login_url='acceso_denegado')
def listfechas(request):
    fecha_actual = timezone.now().date()
    
    disponibilidades = Fecha.objects.filter(
        fecha__gte=fecha_actual,
        disponible=True
    ).order_by('fecha', 'hora')
    
    context = {
        'disponibilidades': disponibilidades
    }
    return render(request, 'listfechas.html', context)

@login_required
@user_passes_test(traer.es_superusuario, login_url='acceso_denegado')
def editarfechas(request, id):
    disponibilidad = Fecha.objects.get(id=id)
    if request.method == 'POST':
        form = FechaForm(request.POST, instance=disponibilidad)
        if form.is_valid():
            form.save()
            return redirect('listfechas')
    else:
        form = FechaForm(instance=disponibilidad)
    return render(request, 'editarfechas.html', {'form': form})

@login_required
@user_passes_test(traer.es_superusuario, login_url='acceso_denegado')
def eliminarfechas(request, id):
    fechaseliminar = get_object_or_404(Fecha, id=id)
    
    if request.method == 'POST':
        fechaseliminar.delete()
        return redirect('listfechas')
    
    return redirect('listfechas')