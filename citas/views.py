from django.conf import settings
from django.contrib import messages
from django.contrib.auth.decorators import login_required, user_passes_test
from django.core.mail import send_mail
from django.http import JsonResponse
from django.shortcuts import render, redirect, get_object_or_404
from django.views.decorators.http import require_POST, require_GET

from inicio.forms import CitaForm
from inicio.models import UserProfile, Cita, Fecha
from inicio import views as traer

@login_required
@user_passes_test(traer.es_superusuario, login_url='acceso_denegado')
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

@login_required
@user_passes_test(traer.es_superusuario, login_url='acceso_denegado')
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
            
            send_mail(
                'Recordatorio de Cita Programada',
                f'Hola {cita.paciente.username},\n\nTu cita ha sido programada para el {cita.fecha_hora.fecha} a las {cita.fecha_hora.hora}.\n\nSaludos,\nTu Equipo de Citas \n Laboratorio Dental - Sandra Gavíria',
                settings.DEFAULT_FROM_EMAIL,
                [cita.paciente.email],
                fail_silently=False,
            )
            
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
    return render(request, 'crearcitas.html', contexto)

@login_required
@user_passes_test(traer.es_superusuario, login_url='acceso_denegado')
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
@user_passes_test(traer.es_superusuario, login_url='acceso_denegado')
@require_GET
def get_horas_disponibles(request):
    fecha = request.GET.get('fecha')
    if fecha:
        try:
            fechas_disponibles = Fecha.objects.filter(fecha=fecha, disponible=True)
            citas_programadas = Cita.objects.filter(fecha_hora__fecha=fecha, estado='programada')
            horas_ocupadas = set(cita.fecha_hora.hora.strftime('%H:%M') for cita in citas_programadas)
            horas_disponibles = set(fecha_hora.hora.strftime('%H:%M') for fecha_hora in fechas_disponibles)
            horas_disponibles -= horas_ocupadas
            return JsonResponse(list(horas_disponibles), safe=False)
        except Exception as e:
            return JsonResponse({'error': str(e)}, status=500)
    return JsonResponse([], safe=False)

@login_required
@user_passes_test(traer.es_superusuario, login_url='acceso_denegado')
def listcitas(request):
    citas = Cita.objects.all() if request.user.is_superuser else Cita.objects.filter(paciente=request.user)
    return render(request, 'listcitas.html', {'citas': citas})

@login_required
@user_passes_test(traer.es_superusuario, login_url='acceso_denegado')
def editarcitas(request, cita_id):
    cita = get_object_or_404(Cita, id=cita_id)
    fecha_hora_original = cita.fecha_hora

    if request.method == 'POST':
        form = CitaForm(request.POST, instance=cita, user=request.user)
        if form.is_valid():
            nueva_cita = form.save(commit=False)
            nueva_fecha = form.cleaned_data['fecha']
            nueva_hora = form.cleaned_data['hora']
            
            nueva_fecha_hora, created = Fecha.objects.get_or_create(fecha=nueva_fecha, hora=nueva_hora)
            
            if nueva_fecha_hora != fecha_hora_original:
                citas_en_fecha_original = Cita.objects.filter(
                    fecha_hora=fecha_hora_original, 
                    estado__in=['programada', 'completada']
                ).exclude(id=cita_id)
                if not citas_en_fecha_original.exists():
                    fecha_hora_original.disponible = True
                    fecha_hora_original.save()
                
                nueva_fecha_hora.disponible = False
                nueva_fecha_hora.save()
                
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
    return render(request, 'editarcitas.html', contexto)