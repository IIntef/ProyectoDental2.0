from django.db.models.signals import post_save, post_delete
from django.dispatch import receiver
from django.contrib.auth.models import User
from django.utils import timezone
from .models import UserProfile, Cita, Fecha

@receiver(post_save, sender=User)
def create_user_profile(sender, instance, created, **kwargs):
    if created:
        UserProfile.objects.create(user=instance)

@receiver(post_save, sender=User)
def save_user_profile(sender, instance, **kwargs):
    instance.userprofile.save()

@receiver(post_save, sender=Cita)
@receiver(post_delete, sender=Cita)
def actualizar_disponibilidad_fecha(sender, instance, **kwargs):
    fecha_hora = instance.fecha_hora
    now = timezone.now()
    
    # Verificar si la fecha y hora son anteriores a la actual
    if fecha_hora.fecha < now.date() or (fecha_hora.fecha == now.date() and fecha_hora.hora < now.time()):
        fecha_hora.disponible = False
    else:
        # La lógica original para fechas futuras
        citas_programadas = Cita.objects.filter(fecha_hora=fecha_hora, estado='programada').exists()
        citas_completadas = Cita.objects.filter(fecha_hora=fecha_hora, estado='completada').exists()
        citas_canceladas = Cita.objects.filter(fecha_hora=fecha_hora, estado='cancelada').exists()

        # La fecha estará disponible si no hay citas programadas activas y no es una fecha pasada
        fecha_hora.disponible = not (citas_programadas or citas_completadas or citas_canceladas)
    
    fecha_hora.save()

# Nueva señal para actualizar todas las fechas periódicamente
@receiver(post_save, sender=Fecha)
def actualizar_todas_fechas(sender, **kwargs):
    now = timezone.now()
    Fecha.objects.filter(fecha__lt=now.date()).update(disponible=False)
    Fecha.objects.filter(fecha=now.date(), hora__lt=now.time()).update(disponible=False)