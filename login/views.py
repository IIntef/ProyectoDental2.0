from django.shortcuts import render, redirect
from django.contrib.auth.forms import UserCreationForm, AuthenticationForm
from django.contrib.auth import login, authenticate, logout
from django.contrib import messages
from django.db import IntegrityError
from .models import *
from django.contrib.auth.decorators import login_required

def newhistoriaclinica(request):
    if request.method == 'POST':
        try:
            user = Valoracion.objects.create(
                tipo=request.POST['type'],
                numero=request.POST['numero'],
                username=request.POST['username'],
                email=request.POST['email'],
            )
            user.save()
            success_message = 'Cuenta Creada Correctamente, Por favor inicie sesión'
        except IntegrityError as e:
            if 'unique constraint' in str(e):
                error_message = 'El usuario ya fue creado'
            else:
                error_message = f'Error al crear el usuario: {e}'

def registrarme(request):
    error_message = None
    success_message = None

    if request.method == 'POST':
        password1 = request.POST.get('password1')
        password2 = request.POST.get('password2')

        if password1 and password2:
            if password1 == password2:
                try:
                    # Verificar si ya existe un usuario con el mismo número de documento
                    existing_user = UserProfile.objects.get(numero=request.POST['numero'])
                    error_message = 'El número de documento ya está en uso'
                except UserProfile.DoesNotExist:
                    try:
                        user = UserProfile.objects.create(
                            tipo=request.POST['type'],
                            numero=request.POST['numero'],
                            username=request.POST['username'],
                            email=request.POST['email'],
                            password=password1
                        )
                        user.set_password(password1)
                        user.save()
                        success_message = 'Cuenta Creada Correctamente, Por favor inicie sesión'
                    except IntegrityError as e:
                        if 'unique constraint' in str(e):
                            error_message = 'El usuario ya fue creado'
                        else:
                            error_message = f'Error al crear el usuario: {e}'
            else:
                error_message = 'Las contraseñas no coinciden'
        else:
            error_message = None

            if request.method == 'POST':
                numero = request.POST.get('numer')
                password = request.POST.get('contra')
                #user = UserProfile.objects.get(numero=numero, password=password)
                user = authenticate(request, username=numero, password=password)
                if user is not None:
                    login(request, user)
                    if numero =='020508'and password=='020508admin':
                        return redirect('dashboardDoc')
                    else:
                        return redirect('dashboard')
                else:
                    error_message = 'Credenciales inválidas'

            context = {
                'error': error_message,
            }
            return render(request, 'loginregister.html', context)

    context = {
        'error': error_message,
        'done': success_message
    }
    return render(request, 'loginregister.html', context)

# ... (el resto de tus vistas)


def loginregister(request):
    return render(request, 'loginregister.html')

def inicio(request):
    return render(request, 'inicio.html')

def signout(request):
    logout(request)
    return redirect('loginregister')

@login_required(login_url='loginregister')
def dashboard(request):
    return render(request, 'dashboard.html')

@login_required(login_url='loginregister')
def dashboardDoc(request):
    return render(request, 'dashboardDoc.html')

@login_required(login_url='loginregister')
def configuracion(request):
    return render(request, 'configuracion.html')

@login_required(login_url='loginregister')
def editaraccount(request):
    return render(request, 'editaraccount.html')

@login_required(login_url='loginregister')
def correo(request):
    return render(request, 'correo.html')

@login_required(login_url='loginregister')
def calendario(request):
    return render(request, 'calendario.html')

@login_required(login_url='loginregister')
def agendarcita(request):
    return render(request, 'agendarcita.html')

@login_required(login_url='loginregister')
def editarcita(request):
    return render(request, 'editarcitas.html')

@login_required(login_url='loginregister')
def newhistoriaclinica(request):
    return render(request, 'newHistoriaClinica.html')

@login_required(login_url='loginregister')
def historias(request):
    return render(request, 'historias.html')

@login_required(login_url='loginregister')
def agregarfechas(request):
    return render(request, 'agregarfechas.html')

def base(request):
    return render(request, 'index.html')
