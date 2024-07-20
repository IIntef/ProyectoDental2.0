from django.contrib import messages
from django.contrib.auth.decorators import login_required, user_passes_test
from django.shortcuts import render, redirect, get_object_or_404

from inicio.forms import ValoracionForm, UserForm
from inicio.models import UserProfile, Valoracion
import inicio.views as traer

@login_required
@user_passes_test(traer.es_superusuario, login_url='acceso_denegado')
def listhistorias(request):
    if request.user.is_superuser:
        historias = Valoracion.objects.all()
    else:
        historias = Valoracion.objects.filter(user=request.user)
    return render(request, 'listhistorias.html', {'historias': historias})

@login_required
@user_passes_test(traer.es_superusuario, login_url='acceso_denegado')
def verhistorias(request, id):
    historia = Valoracion.objects.select_related('user').get(id=id)
    return render(request, 'verhistorias.html', {'historia': historia})

@login_required
@user_passes_test(traer.es_superusuario, login_url='acceso_denegado')
def eliminarhistorias(request, id):
    historiaseliminar = get_object_or_404(Valoracion, id=id)
    
    if request.method == 'POST':
        historiaseliminar.delete()
        return redirect('listhistorias')
    
    return redirect('listhistorias')

@login_required
@user_passes_test(traer.es_superusuario, login_url='acceso_denegado')
def crearhistorias(request):
    if request.method == 'POST':
        numero = request.POST.get('numero')
        user = UserProfile.objects.filter(numero=numero).first()
        
        formularioI = UserForm(request.POST)
        formularioII = ValoracionForm(request.POST)
        
        if user:
            formularioI = UserForm(request.POST, instance=user)
            if formularioI.is_valid() and formularioII.is_valid():
                user = formularioI.save()
                valoracion = formularioII.save(commit=False)
                valoracion.user = user
                valoracion.save()
                messages.success(request, 'Historia clínica creada con éxito.')
                return redirect('listhistorias')
            else:
                print("Errores en formularioI:", formularioI.errors)
                print("Errores en formularioII:", formularioII.errors)
        else:
            messages.error(request, 'El usuario no existe. Por favor, verifique el número ingresado.')
    else:
        formularioI = UserForm()
        formularioII = ValoracionForm()
    
    context = {
        'formularioI': formularioI,
        'formularioII': formularioII
    }
    return render(request, 'crearhistorias.html', context)