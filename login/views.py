from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth.forms import UserCreationForm, AuthenticationForm
from django.contrib.auth import login, authenticate, logout
from django.contrib import messages
from django.db import IntegrityError
from .models import *
from django.contrib.auth.decorators import login_required
from .models import UserProfile, Valoracion
from django.contrib import messages
from django.http import JsonResponse

def registrarme(request):
    error_message = None
    success_message = None

    if request.method == 'POST':
        password1 = request.POST.get('password1')
        password2 = request.POST.get('password2')

        if password1 and password2:
            if password1 == password2:
                try:
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
                user = authenticate(request, username=numero, password=password)
                if user is not None:
                    login(request, user)
                    if numero == '020508' and password == '020508admin':
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

@login_required
def crearhistorias(request):
    if request.method == 'POST':
        numero = request.POST.get('numero')
        user, created = UserProfile.objects.get_or_create(numero=numero)
        
        # Actualizar los datos del usuario
        user.username = request.POST.get('username')
        user.email = request.POST.get('email')
        user.direccion = request.POST.get('direccion')
        user.edad = request.POST.get('edad')
        user.ocupacion = request.POST.get('ocupacion')
        user.celular = request.POST.get('celular')
        user.fecha_ingreso = request.POST.get('fecha_ingreso')
        user.acudiente = request.POST.get('acudiente')
        user.save()

        valoracion = Valoracion(
            user=user,
            tratamiento_medicacion=request.POST.get('tratamiento_medicacion'),
            reacciones_alergicas=request.POST.get('reacciones_alergicas'),
            transtorno_tension_arterial=request.POST.get('transtorno_tension_arterial'),
            diabetes=request.POST.get('diabetes'),
            transtornos_emocionales=request.POST.get('transtornos_emocionales'),
            enfermedad_respiratoria=request.POST.get('enfermedad_respiratoria'),
            otros=request.POST.get('otros'),
            protesis_dental=request.POST.get('protesis_dental'),
            total=request.POST.get('total'),
            acrilico=request.POST.get('acrilico'),
            flexible=request.POST.get('flexible'),
            parcial=request.POST.get('parcial'),
            retenedores=request.POST.get('retenedores'),
            panoramica=request.POST.get('panoramica'),
            periapical=request.POST.get('periapical'),
            cepillado_dental=request.POST.get('cepillado_dental'),
            seda_dental=request.POST.get('seda_dental'),
            enjuague_bucal=request.POST.get('enjuague_bucal'),
        )
        valoracion.save()

        messages.success(request, 'Historia clínica guardada exitosamente.')
        return redirect('dashboardDoc')  
    
    elif request.method == 'GET':
        if request.headers.get('X-Requested-With') == 'XMLHttpRequest':
            numero = request.GET.get('numero')
            user = UserProfile.objects.filter(numero=numero).first()
            if user:
                data = {
                    'username': user.username,
                    'email': user.email,
                    'direccion': user.direccion,
                    'edad': user.edad,
                    'ocupacion': user.ocupacion,
                    'celular': user.celular,
                    'fecha_ingreso': user.fecha_ingreso.strftime('%Y-%m-%d') if user.fecha_ingreso else '',
                    'acudiente': user.acudiente,
                }
                return JsonResponse(data)
            return JsonResponse({}, status=404)
    
    return render(request, 'historiaclinica/formshistorias.html')

def base(request):
    return render(request, 'index.html')

def loginregister(request):
    return render(request, 'loginregister.html')

def inicio(request):
    return render(request, 'inicio.html')

def signout(request):
    logout(request)
    return redirect('loginregister')

@login_required()
def dashboard(request):
    return render(request, 'dashboard.html')

@login_required()
def dashboardDoc(request):
    return render(request, 'dashboardDoc.html')

@login_required()
def configuracion(request):
    return render(request, 'configuracion.html')

@login_required()
def crearcitas(request):
    return render(request, 'citas/crearcitas.html')

@login_required()
def listcitas(request):
    return render(request, 'citas/listcitas.html')

@login_required()
def editarcitas(request):
    return render(request, 'citas/editarcitas.html')

@login_required()
def crearcuentas(request):
    return render(request, 'cuentas/crearcuentas.html')

@login_required()
def listcuentas(request):
    return render(request, 'cuentas/listcuentas.html')

@login_required()
def editarcuentas(request):
    return render(request, 'cuentas/editarcuentas.html')

@login_required()
def crearfechas(request):
    return render(request, 'fechas/crearfechas.html')

@login_required()
def listfechas(request):
    return render(request, 'fechas/listfechas.html')

@login_required()
def editarfechas(request):
    return render(request, 'fechas/editarfechas.html')

@login_required()
def listhistorias(request):
    return render(request, 'historiaclinica/listhistorias.html')

@login_required()
def editarhistorias(request):
    return render(request, 'historiaclinica/editarhistorias.html')

@login_required()
def crearelemento(request):
    return render(request, 'inventario/crearelemento.html')

@login_required()
def listelemento(request):
    return render(request, 'inventario/listelemento.html')

@login_required()
def editarelemento(request):
    return render(request, 'inventario/editarelemento.html')

@login_required()
def correo(request):
    return render(request, 'correo.html')

@login_required()
def calendario(request):
    return render(request, 'calendario.html')