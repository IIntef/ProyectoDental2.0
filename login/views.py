from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth import login, authenticate, logout
from django.db import IntegrityError
from django.core.mail import send_mail, EmailMessage
from django.contrib.auth.tokens import default_token_generator
from django.utils.http import urlsafe_base64_encode, urlsafe_base64_decode
from django.utils.encoding import force_bytes, force_str
from django.urls import reverse
from django.http import HttpResponse, JsonResponse
from django.template.loader import render_to_string
from django.contrib.auth import update_session_auth_hash
from django.contrib.auth.forms import PasswordChangeForm
from django.contrib import messages
from django.contrib.auth.decorators import login_required, user_passes_test
from django.views.decorators.http import require_POST, require_GET
from .models import UserProfile, Valoracion, Inventario, Fecha, Cita
from .forms import ValoracionForm, UserForm, InventarioForm, FechaForm, CitaForm
from django.utils import timezone


def es_superusuario(user):
    return user.is_superuser

def acceso_denegado(request):
    return render(request, 'acceso_denegado.html')

@login_required
def cambiar_password(request):
    if request.method == 'POST':
        form = PasswordChangeForm(request.user, request.POST)
        if form.is_valid():
            user = form.save()
            update_session_auth_hash(request, user)  # Importante para mantener la sesión del usuario
            messages.success(request, 'Tu contraseña ha sido actualizada con éxito!')
            return redirect('dashboard')  # O la página que prefieras
    else:
        form = PasswordChangeForm(request.user)
    return render(request, 'cuentas/cambiar_password.html', {
        'form': form
    })

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
    if request.user.is_superuser:
        historias = Valoracion.objects.all()
    else:
        historias = Valoracion.objects.filter(user=request.user)
    return render(request, 'historiaclinica/listhistorias.html', {'historias': historias})

@user_passes_test(es_superusuario, login_url='acceso_denegado')
@login_required
def verhistorias(request, id):
    historia = Valoracion.objects.select_related('user').get(id=id)
    return render(request, 'historiaclinica/verhistorias.html', {'historia': historia})

@login_required
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
                'acudiente': user.acudiente,
            }
            return JsonResponse(data)
    return JsonResponse({}, status=404)

@user_passes_test(es_superusuario, login_url='acceso_denegado')
@login_required
def eliminarhistorias(request, id):
    historiaseliminar = get_object_or_404(Valoracion, id=id)
    
    if request.method == 'POST':
        historiaseliminar.delete()
        return redirect('listhistorias')
    
    return redirect('listhistorias')

@user_passes_test(es_superusuario, login_url='acceso_denegado')
@login_required
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
    return render(request, 'historiaclinica/crearhistorias.html', context)

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
    if request.user.is_authenticated:
        return render(request, 'dashboard.html', {'user': request.user})
    else:
        return redirect('loginregister')

@login_required()
def configuracion(request, id):
    perfil_usuario = UserProfile.objects.get(id=id)
    if request.method == 'POST':
        form = UserForm(request.POST, request.FILES, instance=perfil_usuario)
        if form.is_valid():
            form.save()
            return redirect('dashboard') 
    else:
        form = UserForm(instance=perfil_usuario)
    return render(request, 'cuentas/configuracion.html', {'form': form})

@login_required
@require_POST
def cancelar_cita(request, cita_id):
    try:
        cita = Cita.objects.get(id=cita_id)
        resultado = cita.cancelar_cita()
        if resultado:
            print(f"Cita {cita_id} cancelada. Nueva disponibilidad: {cita.fecha_hora.disponible}")
            return JsonResponse({'status': 'success'}, status=200)
        else:
            return JsonResponse({'status': 'error', 'message': 'No se pudo cancelar la cita'}, status=400)
    except Cita.DoesNotExist:
        return JsonResponse({'status': 'error', 'message': 'Cita no encontrada'}, status=404)
    except Exception as e:
        print(f"Error al cancelar cita: {str(e)}")
        return JsonResponse({'status': 'error', 'message': str(e)}, status=500)


@login_required()
def crearcitas(request):
    try:
        user_profile = UserProfile.objects.get(numero=request.user.numero)
    except UserProfile.DoesNotExist:
        messages.error(request, 'No se encontró el perfil de usuario.')
        return redirect('listcitas')

    cita_programada = Cita.objects.filter(paciente=user_profile, estado='programada').exists()

    if cita_programada and not request.user.is_superuser:
        messages.error(request, 'Ya tienes una cita programada.')
        return redirect('listcitas')

    if request.method == 'POST':
        formulario = CitaForm(request.POST, user=request.user)
        if formulario.is_valid():
            cita = formulario.save(commit=False)

            if not request.user.is_superuser:
                cita.paciente = user_profile
            cita.estado = 'programada'
            cita.save()
            cita_db = Cita.objects.get(pk=cita.pk)
            fecha_hora_db = Fecha.objects.get(pk=cita.fecha_hora.pk)
            print(f"Estado de la cita después de guardar: {cita_db.estado}")
            print(f"Disponibilidad de fecha_hora después de guardar cita: {fecha_hora_db.disponible}")
            messages.success(request, 'Cita creada exitosamente.')
            return redirect('listcitas')
        else:
            messages.error(request, 'Hubo un problema al crear la cita.')
            print("Errores en formulario:", formulario.errors)
    else:
        formulario = CitaForm(user=request.user)

    contexto = {
        'form': formulario,
        'titulo_formulario': 'Crear Cita' if not cita_programada else 'Editar Cita',
        'is_superuser': request.user.is_superuser,
    }
    return render(request, 'citas/crearcitas.html', contexto)

@login_required
@require_POST
def confirmar_actualizacion_cita(request, cita_id):
    try:
        cita = Cita.objects.get(id=cita_id)
        resultado = cita.confirmar_actualizacion()
        if resultado:
            return JsonResponse({'status': 'success'}, status=200)
        else:
            return JsonResponse({'status': 'error', 'message': 'No se pudo actualizar la cita'}, status=400)
    except Cita.DoesNotExist:
        return JsonResponse({'status': 'error', 'message': 'Cita no encontrada'}, status=404)
    except Exception as e:
        return JsonResponse({'status': 'error', 'message': str(e)}, status=500)

@login_required
@require_GET
def get_horas_disponibles(request):
    fecha = request.GET.get('fecha')
    if fecha:
        try:
            # Filtra las fechas disponibles para la fecha específica
            fechas_disponibles = Fecha.objects.filter(fecha=fecha, disponible=True)
            # Obtén las horas ya ocupadas para esa fecha
            citas_programadas = Cita.objects.filter(fecha_hora__fecha=fecha, estado='programada')
            horas_ocupadas = set(cita.fecha_hora.hora.strftime('%H:%M') for cita in citas_programadas)
            # Crea un conjunto de horas disponibles
            horas_disponibles = set(fecha_hora.hora.strftime('%H:%M') for fecha_hora in fechas_disponibles)
            # Filtra las horas disponibles excluyendo las ocupadas
            horas_disponibles -= horas_ocupadas
            return JsonResponse(list(horas_disponibles), safe=False)
        except Exception as e:
            return JsonResponse({'error': str(e)}, status=500)
    # Si no se proporciona una fecha válida, devuelve una lista vacía
    return JsonResponse([], safe=False)

@login_required()
def listcitas(request):
    if request.user.is_superuser:
        citas = Cita.objects.all()
    else:
        citas = Cita.objects.filter(paciente=request.user)
    return render(request, 'citas/listcitas.html', {'citas': citas})

@login_required()
def editarcitas(request, cita_id):
    cita = get_object_or_404(Cita, id=cita_id)
    fecha_hora_original = cita.fecha_hora

    if request.method == 'POST':
        form = CitaForm(request.POST, instance=cita, user=request.user)
        if form.is_valid():
            nueva_cita = form.save(commit=False)
            nueva_fecha = form.cleaned_data['fecha']
            nueva_hora = form.cleaned_data['hora']
            
            # Obtener o crear el objeto Fecha para la nueva fecha y hora
            nueva_fecha_hora, created = Fecha.objects.get_or_create(fecha=nueva_fecha, hora=nueva_hora)
            
            if nueva_fecha_hora != fecha_hora_original:
                print(f"Editando cita de {fecha_hora_original} a {nueva_fecha_hora}")
                
                # Liberar la fecha original
                citas_en_fecha_original = Cita.objects.filter(
                    fecha_hora=fecha_hora_original, 
                    estado__in=['programada', 'completada']
                ).exclude(id=cita_id)
                if not citas_en_fecha_original.exists():
                    fecha_hora_original.disponible = True
                    fecha_hora_original.save()
                    print(f"Fecha original {fecha_hora_original} marcada como disponible")
                
                # Ocupar la nueva fecha
                nueva_fecha_hora.disponible = False
                nueva_fecha_hora.save()
                print(f"Nueva fecha {nueva_fecha_hora} marcada como no disponible")
                
                nueva_cita.fecha_hora = nueva_fecha_hora
            
            nueva_cita.save()
            messages.success(request, 'Cita actualizada exitosamente.')
            return redirect('listcitas')
        else:
            print(form.errors)
    else:
        initial_data = {
            'fecha': cita.fecha_hora.fecha,
            'hora': cita.fecha_hora.hora,
            'motivo': cita.motivo,
            'paciente': cita.paciente
        }
        form = CitaForm(instance=cita, user=request.user, initial=initial_data)

    contexto = {
        'form': form,
        'cita': cita,
    }
    return render(request, 'citas/editarcitas.html', contexto)

@user_passes_test(es_superusuario, login_url='acceso_denegado')
@login_required()
@require_POST
@user_passes_test(lambda u: u.is_superuser)  # Asegura que solo el admin pueda actualizar la asistencia
def actualizar_asistencia(request, cita_id):
    cita = get_object_or_404(Cita, id=cita_id)
    
    # Actualiza el estado de la cita a "Completada"
    cita.estado = 'completada'
    cita.save()

    return HttpResponse(status=200)

@user_passes_test(es_superusuario, login_url='acceso_denegado')
@login_required()
def crearcuentas(request):
    if request.method == 'POST':
        form = UserForm(request.POST, request.FILES)
        if form.is_valid():
            form.save()
            return redirect('listcuentas')  
    else:
        form = UserForm()
    
    return render(request, 'cuentas/crearcuentas.html', {'form': form})

@user_passes_test(es_superusuario, login_url='acceso_denegado')
@login_required
def listcuentas(request):
    cuentas= UserProfile.objects.all()
    return render(request, 'cuentas/listcuentas.html', {'cuentas': cuentas})

@user_passes_test(es_superusuario, login_url='acceso_denegado')
@login_required
def editarcuentas(request, id):
    form_edcuentas = UserProfile.objects.get(id=id)
    if request.method == 'POST':
        form = UserForm(request.POST, request.FILES, instance=form_edcuentas)
        if form.is_valid():
            form.save()
            return redirect('listcuentas') 
    else:
        form = UserForm(instance=form_edcuentas)
    return render(request, 'cuentas/editarcuentas.html', {'form': form})

@user_passes_test(es_superusuario, login_url='acceso_denegado')
@login_required
def eliminarelementos(request, id):
    elementoseliminar = get_object_or_404(Inventario, id=id)
    
    if request.method == 'POST':
        elementoseliminar.delete()
        return redirect('listelementos')
    
    return redirect('listelementos')

@user_passes_test(es_superusuario, login_url='acceso_denegado')
@login_required()
def crearfechas(request):
    if request.method == 'POST':
        disponibilidad = FechaForm(request.POST)
        if disponibilidad.is_valid():
            disponibilidad.save()
            return redirect('listfechas')
    else:
        form = FechaForm()
    
    return render(request, 'fechas/crearfechas.html', {'form': form})

@user_passes_test(es_superusuario, login_url='acceso_denegado')
@login_required()
def listfechas(request):
    # Obtener la fecha actual
    fecha_actual = timezone.now().date()
    
    # Obtener solo las fechas futuras que están marcadas como disponibles
    disponibilidades = Fecha.objects.filter(
        fecha__gte=fecha_actual,
        disponible=True
    ).order_by('fecha', 'hora')
    
    context = {
        'disponibilidades': disponibilidades
    }
    return render(request, 'fechas/listfechas.html', context)

@user_passes_test(es_superusuario, login_url='acceso_denegado')
@login_required()
def editarfechas(request, id):
    disponibilidad = Fecha.objects.get(id=id)
    if request.method == 'POST':
        form = FechaForm(request.POST, instance=disponibilidad)
        if form.is_valid():
            form.save()
            return redirect('listfechas')
    else:
        form = FechaForm(instance=disponibilidad)
    return render(request, 'fechas/editarfechas.html', {'form': form})

@user_passes_test(es_superusuario, login_url='acceso_denegado')
@login_required
def eliminarfechas(request, id):
    fechaseliminar = get_object_or_404(Fecha, id=id)
    
    if request.method == 'POST':
        fechaseliminar.delete()
        return redirect('listfechas')
    
    return redirect('listfechas')

@user_passes_test(es_superusuario, login_url='acceso_denegado')
@login_required()
def crearelementos(request):
    if request.method == 'POST':
        form = InventarioForm(request.POST, request.FILES)
        if form.is_valid():
            form.save()
            return redirect('listelementos')  
    else:
        form = InventarioForm()
    
    return render(request, 'inventario/crearelementos.html', {'form': form})

@user_passes_test(es_superusuario, login_url='acceso_denegado')
@login_required()
def listelementos(request):
    inventarios= Inventario.objects.all()
    return render(request, 'inventario/listelementos.html', {'inventarios': inventarios})

@user_passes_test(es_superusuario, login_url='acceso_denegado')
@login_required()
def editarelementos(request, id):
    form_edelem = Inventario.objects.get(id=id)
    if request.method == 'POST':
        form = InventarioForm(request.POST, request.FILES, instance=form_edelem)
        if form.is_valid():
            form.save()
            return redirect('listelementos') 
    else:
        form = InventarioForm(instance=form_edelem)
    return render(request, 'inventario/editarelementos.html', {'form': form})

@login_required()
def correo(request):
    return render(request, 'correo.html')

@login_required()
def calendario(request):
    return render(request, 'calendario.html')