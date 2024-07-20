from django.contrib import messages
from django.contrib.auth import update_session_auth_hash
from django.contrib.auth.decorators import login_required, user_passes_test
from django.contrib.auth.forms import PasswordChangeForm
from django.http import JsonResponse
from django.shortcuts import render, redirect, get_object_or_404

from inicio.forms import UserForm
from inicio.models import UserProfile
from inicio import views as traer

@login_required
@user_passes_test(traer.es_superusuario, login_url='acceso_denegado')
def fetch_user_details(request):
    if request.headers.get('X-Requested-With') == 'XMLHttpRequest':
        numero = request.GET.get('numero')
        user = UserProfile.objects.filter(numero=numero).first()
        if user:
            data = {
                'tipo': user.tipo,
                'username': user.username,
                'email': user.email,
                'direccion': user.direccion,
                'edad': user.edad,
                'ocupacion': user.ocupacion,
                'celular': user.celular,
                'acudiente': user.acudiente,
            }
            return JsonResponse(data)
    return JsonResponse({}, status=404)

@login_required
@user_passes_test(traer.es_superusuario, login_url='acceso_denegado')
def crearcuentas(request):
    if request.method == 'POST':
        form = UserForm(request.POST, request.FILES)
        if form.is_valid():
            form.save()
            return redirect('listcuentas')  
    else:
        form = UserForm()
    
    return render(request, 'crearcuentas.html', {'form': form})

@login_required
@user_passes_test(traer.es_superusuario, login_url='acceso_denegado')
def listcuentas(request):
    cuentas = UserProfile.objects.all()
    return render(request, 'listcuentas.html', {'cuentas': cuentas})

@login_required
@user_passes_test(traer.es_superusuario, login_url='acceso_denegado')
def editarcuentas(request, id):
    cuenta = get_object_or_404(UserProfile, id=id)
    if request.method == 'POST':
        form = UserForm(request.POST, request.FILES, instance=cuenta)
        if form.is_valid():
            form.save()
            return redirect('listcuentas')
    else:
        form = UserForm(instance=cuenta)
    return render(request, 'editarcuentas.html', {'form': form})

@login_required
@user_passes_test(traer.es_superusuario, login_url='acceso_denegado')
def cambiar_password(request):
    if request.method == 'POST':
        form = PasswordChangeForm(request.user, request.POST)
        if form.is_valid():
            user = form.save()
            update_session_auth_hash(request, user)
            messages.success(request, 'Tu contraseña ha sido actualizada con éxito!')
            return redirect('dashboard')
    else:
        form = PasswordChangeForm(request.user)
    return render(request, 'cambiar_password.html', {'form': form})