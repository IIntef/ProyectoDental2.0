from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth import login, authenticate, logout
from django.db import IntegrityError
from .models import *
from django.contrib.auth.decorators import login_required
from .models import UserProfile, Valoracion
from django.http import JsonResponse
from .forms import ValoracionForm, UserForm
from django.core.mail import send_mail
from django.contrib.auth.tokens import default_token_generator
from django.utils.http import urlsafe_base64_encode
from django.utils.encoding import force_bytes
from django.urls import reverse
from django.contrib.auth.views import PasswordResetView, PasswordResetDoneView, PasswordResetConfirmView, PasswordResetCompleteView
from django.urls import reverse_lazy

class CustomPasswordResetView(PasswordResetView):
    template_name = 'registration/password_reset_form.html'
    email_template_name = 'registration/password_reset_email.html'
    success_url = reverse_lazy('password_reset_done')

class CustomPasswordResetDoneView(PasswordResetDoneView):
    template_name = 'registration/password_reset_done.html'

class CustomPasswordResetConfirmView(PasswordResetConfirmView):
    template_name = 'registration/password_reset_confirm.html'
    success_url = reverse_lazy('password_reset_complete')

class CustomPasswordResetCompleteView(PasswordResetCompleteView):
    template_name = 'registration/password_reset_complete.html'


def forgot_password(request):
    if request.method == 'POST':
        email = request.POST.get('email')
        user = UserProfile.objects.filter(email=email).first()
        if user:
            # Generar token
            token = default_token_generator.make_token(user)
            uid = urlsafe_base64_encode(force_bytes(user.pk))
            # Construir URL de restablecimiento
            reset_url = request.build_absolute_uri(
                reverse('password_reset_confirm', kwargs={'uidb64': uid, 'token': token})
            )
            # Enviar email
            send_mail(
                'Restablecimiento de contraseña',
                f'Usa este enlace para restablecer tu contraseña: {reset_url}',
                'noreply@tudominio.com',
                [email],
                fail_silently=False,
            )
            return render(request, 'forgot_password.html', {'message': 'Se ha enviado un correo con instrucciones.'})
        else:
            return render(request, 'forgot_password.html', {'error': 'No se encontró un usuario con ese correo.'})
    return render(request, 'forgot_password.html')

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
    if request.user.is_superuser:
        historias = Valoracion.objects.all()
    else:
        historias = Valoracion.objects.filter(user=request.user)
    return render(request, 'historiaclinica/listhistorias.html', {'historias': historias})

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

@login_required
def eliminarhistorias(request, id):
    historiaseliminar = get_object_or_404(Valoracion, id=id)
    
    if request.method == 'POST':
        historiaseliminar.delete()
        return redirect('listhistorias')
    
    return redirect('listhistorias')

@login_required
def crearhistorias(request):
    if request.method == 'POST':
        numero = request.POST.get('numero')
        user = UserProfile.objects.filter(numero=numero).first()
        
        if user:
            formularioI = UserForm(request.POST, instance=user)
        else:
            formularioI = UserForm(request.POST)
        
        formularioII = ValoracionForm(request.POST)
        
        if formularioI.is_valid() and formularioII.is_valid():
            user = formularioI.save()
            valoracion = formularioII.save(commit=False)
            valoracion.user = user
            valoracion.save()
            return redirect('listhistorias')
        else:
            print("Errores en formularioI:", formularioI.errors)
            print("Errores en formularioII:", formularioII.errors)
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
def dashboardDoc(request):
    if request.user.is_authenticated:
        return render(request, 'dashboardDoc.html', {'user': request.user})
    else:
        return redirect('loginregister')

@login_required()
def configuracion(request, id):
    perfil_usuario = UserProfile.objects.get(id=id)
    if request.method == 'POST':
        form = UserForm(request.POST, request.FILES, instance=perfil_usuario)
        if form.is_valid():
            form.save()
            return redirect('listcuentas') 
    else:
        form = UserForm(instance=perfil_usuario)
    return render(request, 'configuracion.html', {'form': form})

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
    if request.method == 'POST':
        form = UserForm(request.POST, request.FILES)
        if form.is_valid():
            form.save()
            return redirect('listcuentas')  
    else:
        form = UserForm()
    
    return render(request, 'cuentas/crearcuentas.html', {'form': form})

@login_required
def listcuentas(request):
    cuentas= UserProfile.objects.all()
    return render(request, 'cuentas/listcuentas.html', {'cuentas': cuentas})

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