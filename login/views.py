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
from .forms import ValoracionForm, UserForm

def registrarme(request):
    error_message = None
    success_message = None

    if request.method == 'POST':
        if 'password1' in request.POST:
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
            numero = request.POST.get('numer')
            password = request.POST.get('contra')
            user = authenticate(request, username=numero, password=password)
            if user is not None:
                login(request, user)
                if user.is_superuser:
                    return redirect('dashboardDoc')
                else:
                    return redirect('dashboard')
            else:
                error_message = 'Credenciales inválidas'

    context = {
        'error': error_message,
        'done': success_message
    }
    return render(request, 'loginregister.html', context)

@login_required
def listhistorias(request):
    historias= Valoracion.objects.all()
    return render(request, 'historiaclinica/listhistorias.html', {'historias': historias})

@login_required
def verhistorias(request, id):
    historia = Valoracion.objects.select_related('user').get(id=id)
    return render(request, 'historiaclinica/verhistorias.html', {'historia': historia})

def fetch_user_details(request):
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

@login_required
def eliminarhistorias (request, id):
    historiaseliminar= Valoracion.objects.get(id=id)
    historiaseliminar.delete()
    return  redirect('listhistorias')

@login_required
def crearhistorias(request):
    formularioI = UserForm(request.POST or None, request.FILES or None)
    formularioII = ValoracionForm(request.POST or None, request.FILES or None)
    
    if formularioI.is_valid() and formularioII.is_valid():
        user = formularioI.save()  # This will update the existing user
        valoracion = formularioII.save(commit=False)
        valoracion.user = user
        valoracion.save()
        return redirect('listhistorias')
        
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
                'acudiente': user.acudiente,
            }
            return JsonResponse(data)
        return JsonResponse({}, status=404)
    
    context = {
        'formularioI': formularioI,
        'formularioII': formularioII
    }
    return render(request, 'historiaclinica/crearhistorias.html', context)


def crear(request):
    formulario= LibroForm(request.POST or None, request.FILES or None)
    if formulario.is_valid():
        formulario.save()
        return redirect('libros')
    return render(request, 'libros/crear.html', {'formulario': formulario})

@login_required
def libros(request):
    libros= libro.objects.all()
    return render(request, 'libros/indes.html', {'libros': libros})

@login_required
def editar(request, id):
    libro_ed = libro.objects.get(id=id)
    formulario = LibroForm(request.POST or None, request.FILES or None, instance=libro_ed) 
    if formulario.is_valid():
        formulario.save()
        return redirect('libros')   
    return render(request, 'libros/editar.html', { 'formulario': formulario})

@login_required
def eliminar (request, id):
    libroe= libro.objects.get(id=id)
    libroe.delete()
    return  redirect('libros')


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