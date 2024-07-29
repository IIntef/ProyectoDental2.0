import os
from datetime import datetime, timedelta

from django.conf import settings
from django.contrib import messages
from django.contrib.auth.decorators import login_required, user_passes_test
from django.core.mail import send_mail
from django.http import JsonResponse, HttpResponseRedirect
from django.shortcuts import render, redirect, get_object_or_404
from django.views.decorators.http import require_POST, require_GET
from django.urls import reverse
from google_auth_oauthlib.flow import Flow
from google.oauth2.credentials import Credentials
from googleapiclient.discovery import build
from googleapiclient.errors import HttpError
from django.utils import timezone

from inicio.forms import CitaForm
from inicio.models import UserProfile, Cita, Fecha
from inicio import views as traer

CLIENT_SECRETS_FILE = os.path.join(settings.BASE_DIR, 'config/credentials.json')
SCOPES = ['https://www.googleapis.com/auth/calendar', 'https://www.googleapis.com/auth/calendar.readonly']

def get_google_calendar_service(request):
    if 'credentials' not in request.session:
        return redirect('initiate_oauth')
    
    credentials = Credentials(**request.session['credentials'])
    
    if not credentials.valid:
        if credentials.expired and credentials.refresh_token:
            credentials.refresh(Request())
            request.session['credentials'] = {
                'token': credentials.token,
                'refresh_token': credentials.refresh_token,
                'token_uri': credentials.token_uri,
                'client_id': credentials.client_id,
                'client_secret': credentials.client_secret,
                'scopes': credentials.scopes
            }
        else:
            return redirect('initiate_oauth')
    
    return build('calendar', 'v3', credentials=credentials)

def initiate_oauth(request):
    redirect_uri = request.build_absolute_uri(reverse('oauth2callback'))
    print(f"Redirect URI: {redirect_uri}")
    flow = Flow.from_client_secrets_file(
        CLIENT_SECRETS_FILE,
        scopes=SCOPES,
        redirect_uri=redirect_uri
    )
    authorization_url, state = flow.authorization_url(
        access_type='offline',
        include_granted_scopes='true',
    )
    request.session['state'] = state
    print(f"Authorization URL: {authorization_url}")
    return redirect(authorization_url)

import os
from google_auth_oauthlib.flow import Flow
from django.shortcuts import redirect
from django.urls import reverse
from django.contrib import messages

def oauth2callback(request):
    os.environ['OAUTHLIB_INSECURE_TRANSPORT'] = '1'
    os.environ['OAUTHLIB_RELAX_TOKEN_SCOPE'] = '1'
    
    redirect_uri = request.build_absolute_uri(reverse('oauth2callback'))
    print(f"Redirect URI in oauth2callback: {redirect_uri}")
    print(f"Full request URL: {request.build_absolute_uri()}")
    
    state = request.session.get('state')
    if not state:
        return redirect('initiate_oauth')
    
    flow = Flow.from_client_secrets_file(
        CLIENT_SECRETS_FILE,
        scopes=SCOPES,
        state=state,
        redirect_uri=redirect_uri
    )
    
    try:
        flow.fetch_token(authorization_response=request.build_absolute_uri())
        credentials = flow.credentials
        
        request.session['credentials'] = {
            'token': credentials.token,
            'refresh_token': credentials.refresh_token,
            'token_uri': credentials.token_uri,
            'client_id': credentials.client_id,
            'client_secret': credentials.client_secret,
            'scopes': credentials.scopes
        }
        
        messages.success(request, 'Autenticación con Google Calendar completada exitosamente.')
        return redirect('listcitas')
    
    except Warning as w:
        print(f"Advertencia durante la autenticación: {str(w)}")
        messages.warning(request, f'Se produjo una advertencia durante la autenticación: {str(w)}')
        # Puedes decidir continuar o manejar esto de otra manera
        return redirect('listcitas')
    
    except Exception as e:
        print(f"Error durante la autenticación: {str(e)}")
        messages.error(request, f'Error durante la autenticación: {str(e)}')
        return redirect('initiate_oauth')

@login_required(login_url='acceso_denegado')
@require_POST
def cancelar_cita(request, cita_id):
    try:
        cita = Cita.objects.get(id=cita_id)
        resultado = cita.cancelar_cita()
        if resultado:
            # Eliminar el evento de Google Calendar
            service = get_google_calendar_service(request)
            if isinstance(service, HttpResponseRedirect):
                return service  # Esto redirigirá al usuario a la página de autorización de Google

            # Buscar el evento por su descripción (asumiendo que guardamos el ID de la cita en la descripción)
            events_result = service.events().list(calendarId='primary', q=f'Cita ID: {cita_id}').execute()
            events = events_result.get('items', [])

            if events:
                event = events[0]
                service.events().delete(calendarId='primary', eventId=event['id']).execute()
                print(f"Evento de Google Calendar eliminado para la cita {cita_id}")
                
            # Enviar correo
            recipient_list = [cita.paciente.email, "facturacionldsg@gmail.com"]
            send_mail(
                'Cita Cancelada',
                f'Hola {cita.paciente.username},\n\nTu cita para el {cita.fecha_hora} ha sido cancelada .\nSi deseas agendar otra cita ingresa a nuestra plataforma. \n\n Saludos,\nTu Equipo de Citas \n Laboratorio Dental - Sandra Gavíria',
                settings.DEFAULT_FROM_EMAIL,
                recipient_list,
                fail_silently=False,
            )
            
            print(f"Cita {cita_id} cancelada. Nueva disponibilidad: {cita.fecha_hora.disponible}")
            return JsonResponse({'status': 'success'}, status=200)
        else:
            return JsonResponse({'status': 'error', 'message': 'No se pudo cancelar la cita'}, status=400)
    except Cita.DoesNotExist:
        return JsonResponse({'status': 'error', 'message': 'Cita no encontrada'}, status=404)
    except Exception as e:
        print(f"Error al cancelar cita: {str(e)}")
        return JsonResponse({'status': 'error', 'message': str(e)}, status=500)


@login_required(login_url='acceso_denegado')
def crearcitas(request):
    if request.method == 'POST':
        formulario = CitaForm(request.POST, user=request.user)
        if formulario.is_valid():
            paciente = formulario.cleaned_data['paciente'] if request.user.is_superuser else request.user

            # Verificar si el paciente ya tiene una cita programada
            cita_programada = Cita.objects.filter(paciente=paciente, estado='Programada').exists()

            if cita_programada:
                messages.error(request, f'El paciente {paciente.username} ya tiene una cita programada.')
                return redirect('listcitas')

            cita = formulario.save(commit=False)
            cita.paciente = paciente
            cita.estado = 'programada'
            cita.save()

            # Enviar correo
            recipient_list = [cita.paciente.email, "facturacionldsg@gmail.com"]
            send_mail(
                'Recordatorio de Cita Programada',
                f'Hola {cita.paciente.username},\n\nTu cita ha sido programada para el {cita.fecha_hora}.\n\nSaludos,\nTu Equipo de Citas \n Laboratorio Dental - Sandra Gavíria',
                settings.DEFAULT_FROM_EMAIL,
                recipient_list,
                fail_silently=False,
            )

            # Crear evento en Google Calendar
            service = get_google_calendar_service(request)
            if isinstance(service, HttpResponseRedirect):
                return service  # Esto redirigirá al usuario a la página de autorización de Google

            fecha = formulario.cleaned_data['fecha']
            hora = formulario.cleaned_data['hora']
            fecha_datetime = datetime.combine(fecha, hora)
            
            event = {
                'summary': 'Cita Programada',
                'location': 'Tu ubicación aquí',
                'description': f'Cita ID: {cita.id}\nCita programada para {cita.paciente.username}',
                'start': {
                    'dateTime': fecha_datetime.isoformat(),
                    'timeZone': 'America/Bogota',
                },
                'end': {
                    'dateTime': (fecha_datetime + timedelta(hours=1)).isoformat(),
                    'timeZone': 'America/Bogota',
                },
                'attendees': [
                    {'email': cita.paciente.email},
                    {'email': "facturacionldsg@gmail.com"},
                ],
                'reminders': {
                    'useDefault': False,
                    'overrides': [
                        {'method': 'email', 'minutes': 24 * 60},
                        {'method': 'popup', 'minutes': 10},
                    ],
                },
            }

            try:
                created_event = service.events().insert(calendarId='primary', body=event).execute()
                cita.google_event_id = created_event['id']
                cita.save()
                print('Evento creado: %s' % (created_event.get('htmlLink')))
                messages.success(request, 'Cita creada exitosamente y evento añadido a Google Calendar.')
            except HttpError as e:
                print(f"Error al crear evento en Google Calendar: {str(e)}")
                messages.warning(request, 'Cita creada exitosamente, pero hubo un problema al añadir el evento a Google Calendar.')

            return redirect('listcitas')
        else:
            messages.error(request, 'Hubo un problema al crear la cita.')
            print("Errores en formulario:", formulario.errors)
    else:
        formulario = CitaForm(user=request.user)

    contexto = {
        'form': formulario,
        'titulo_formulario': 'Crear Cita',
        'is_superuser': request.user.is_superuser,
    }
    return render(request, 'crearcitas.html', contexto)

@login_required
@user_passes_test(traer.es_superusuario, login_url='acceso-denegado')
@require_POST
def confirmar_actualizacion_cita(request, cita_id):
    try:
        cita = Cita.objects.get(id=cita_id)
        resultado = cita.confirmar_actualizacion()
        if resultado:
            # Eliminar el evento de Google Calendar
            service = get_google_calendar_service(request)
            if isinstance(service, HttpResponseRedirect):
                return service  # Esto redirigirá al usuario a la página de autorización de Google

            # Buscar el evento por su descripción (asumiendo que guardamos el ID de la cita en la descripción)
            events_result = service.events().list(calendarId='primary', q=f'Cita ID: {cita_id}').execute()
            events = events_result.get('items', [])

            if events:
                event = events[0]
                service.events().delete(calendarId='primary', eventId=event['id']).execute()
                print(f"Evento de Google Calendar eliminado para la cita {cita_id}")
            
            print(f"Cita {cita_id} Completada.")
    
        if resultado:
            return JsonResponse({'status': 'success'}, status=200)
        else:
            return JsonResponse({'status': 'error', 'message': 'No se pudo actualizar la cita'}, status=400)
    except Cita.DoesNotExist:
        return JsonResponse({'status': 'error', 'message': 'Cita no encontrada'}, status=404)
    except Exception as e:
        return JsonResponse({'status': 'error', 'message': str(e)}, status=500)

@login_required(login_url='acceso_denegado')
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

@login_required(login_url='acceso_denegado')
def listcitas(request):
    Cita.objects.filter(
        fecha_hora__fecha__lt=timezone.now().date(),
        estado='programada'
    ).update(estado='inasistida')
    citas = Cita.objects.all() if request.user.is_superuser else Cita.objects.filter(paciente=request.user)
    return render(request, 'listcitas.html', {'citas': citas})

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
                
                # Enviar correo
                recipient_list = [cita.paciente.email, "facturacionldsg@gmail.com"]
                send_mail(
                    'Cita ReAgendada',
                    f'Hola {cita.paciente.username},\n\nTu cita para el {fecha_hora_original} ha sido reagendada para el {nueva_fecha_hora}.\n\n Saludos,\nTu Equipo de Citas \n Laboratorio Dental - Sandra Gavíria',
                    settings.DEFAULT_FROM_EMAIL,
                    recipient_list,
                    fail_silently=False,
                )
            
                nueva_cita.fecha_hora = nueva_fecha_hora

                # Eliminar el evento viejo en Google Calendar
                service = get_google_calendar_service(request)
                if isinstance(service, HttpResponseRedirect):
                    return service

                if cita.google_event_id:
                    try:
                        service.events().delete(calendarId='primary', eventId=cita.google_event_id).execute()
                        print(f"Evento de Google Calendar eliminado para la cita {cita_id}")
                    except HttpError as e:
                        print(f"Error al eliminar el evento: {str(e)}")

            nueva_cita.save()

            # Crear un nuevo evento en Google Calendar
            fecha_datetime = datetime.combine(nueva_fecha, nueva_hora)
            event = {
                'summary': 'Cita Programada',
                'location': 'Tu ubicación aquí',
                'description': f'Cita ID: {nueva_cita.id}\nCita programada para {nueva_cita.paciente.username}',
                'start': {
                    'dateTime': fecha_datetime.isoformat(),
                    'timeZone': 'America/Bogota',
                },
                'end': {
                    'dateTime': (fecha_datetime + timedelta(hours=1)).isoformat(),
                    'timeZone': 'America/Bogota',
                },
                'attendees': [
                    {'email': nueva_cita.paciente.email},
                    {'email': request.user.email},
                ],
                'reminders': {
                    'useDefault': False,
                    'overrides': [
                        {'method': 'email', 'minutes': 24 * 60},
                        {'method': 'popup', 'minutes': 10},
                    ],
                },
            }

            try:
                new_event = service.events().insert(calendarId='primary', body=event).execute()
                print('Nuevo evento creado: %s' % (new_event.get('htmlLink')))
                nueva_cita.google_event_id = new_event['id']
                nueva_cita.save()
                messages.success(request, 'Cita actualizada exitosamente y evento de Google Calendar actualizado.')
            except HttpError as e:
                print(f"Error al crear nuevo evento en Google Calendar: {str(e)}")
                messages.warning(request, 'Cita actualizada exitosamente, pero hubo un problema al añadir el evento a Google Calendar.')

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


