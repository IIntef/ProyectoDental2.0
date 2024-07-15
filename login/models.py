from django.db import models
from django.contrib.auth.models import AbstractBaseUser, BaseUserManager, PermissionsMixin

class UserProfileManager(BaseUserManager):
    def create_user(self, numero, username, email, password=None, tipo=2):
        if not numero:
            raise ValueError('Users must have a document number')
        if not email:
            raise ValueError('Users must have an email address')

        user = self.model(
            numero=numero,
            username=username,
            email=self.normalize_email(email),
            tipo=tipo
        )
        user.set_password(password)
        user.save(using=self._db)
        return user

    def create_superuser(self, numero, username, email, password=None, tipo=2):
        user = self.create_user(
            numero=numero,
            username=username,
            email=email,
            password=password,
            tipo=tipo,
        )
        user.is_admin = True
        user.is_staff = True
        user.is_superuser = True
        user.save(using=self._db)
        return user

class UserProfile(AbstractBaseUser, PermissionsMixin):
    TIPO_CHOICES = (
        (1, 'T.I'),
        (2, 'C.C'),
        (3, 'C.E'),
        (4, 'C.I'),
    )
    
    tipo = models.PositiveSmallIntegerField(choices=TIPO_CHOICES, default=2)
    numero = models.PositiveIntegerField(unique=True)
    username = models.CharField(max_length=50)
    imagen = models.ImageField(upload_to='imagenes/', blank=True, null=True)
    direccion = models.CharField(max_length=100, null=True, blank=True)
    email = models.EmailField(max_length=100, null=True, blank=True, unique=True)
    ocupacion = models.CharField(max_length=50, null=True, blank=True)
    celular = models.CharField(max_length=15, null=True, blank=True)  # Changed to CharField
    acudiente = models.CharField(max_length=50, null=True, blank=True)  # Changed default to blank=True
    edad = models.PositiveSmallIntegerField(null=True, blank=True)
    is_active = models.BooleanField(default=True, null=True, blank=True)
    is_staff = models.BooleanField(default=False, null=True, blank=True)
    is_admin = models.BooleanField(default=False, null=True, blank=True)
    is_superuser = models.BooleanField(default=False, null=True, blank=True)

    objects = UserProfileManager()

    USERNAME_FIELD = 'numero'
    REQUIRED_FIELDS = ['username', 'email']

    def __str__(self):
        return str(self.numero)

class Valoracion(models.Model):  # Changed to PascalCase
    OPCIONES_SI_NO_NO_SABE = (
        (1, 'Si'),
        (2, 'No'),
        (3, 'Desinformado'),
    )
    OPCIONES_SI_NO = (
        (1, 'Si'),
        (2, 'No'),
    )

    user = models.ForeignKey(UserProfile, on_delete=models.CASCADE)
    username = models.CharField(max_length=150, blank=True) 
    numero = models.CharField(max_length=50, blank=True) 
    fecha_historia = models.DateField(null=True, blank=True) 
    tratamiento_medicacion = models.PositiveSmallIntegerField(choices=OPCIONES_SI_NO_NO_SABE, default=3)
    reacciones_alergicas = models.PositiveSmallIntegerField(choices=OPCIONES_SI_NO_NO_SABE, default=3)
    transtorno_tension_arterial = models.PositiveSmallIntegerField(choices=OPCIONES_SI_NO_NO_SABE, default=3)
    diabetes = models.PositiveSmallIntegerField(choices=OPCIONES_SI_NO_NO_SABE, default=3)
    transtornos_emocionales = models.PositiveSmallIntegerField(choices=OPCIONES_SI_NO_NO_SABE, default=3)
    enfermedad_respiratoria = models.PositiveSmallIntegerField(choices=OPCIONES_SI_NO_NO_SABE, default=3)
    otros = models.CharField(max_length=100, blank=True)

    protesis_dental = models.CharField(max_length=100, blank=True)
    total = models.CharField(max_length=100, blank=True)
    acrilico = models.CharField(max_length=100, blank=True)
    flexible = models.CharField(max_length=100, blank=True)
    parcial = models.CharField(max_length=100, blank=True)
    retenedores = models.CharField(max_length=100, blank=True)

    panoramica = models.CharField(max_length=100, blank=True)
    periapical = models.CharField(max_length=100, blank=True)

    cepillado_dental = models.PositiveSmallIntegerField(choices=OPCIONES_SI_NO)
    seda_dental = models.PositiveSmallIntegerField(choices=OPCIONES_SI_NO)
    enjuague_bucal = models.PositiveSmallIntegerField(choices=OPCIONES_SI_NO)

    def save(self, *args, **kwargs):
        if self.user:
            self.username = self.user.username
            self.numero = self.user.numero
        super().save(*args, **kwargs)

    def __str__(self):
        return f"Valoración de {self.username} (Número: {self.numero})"
    

class Inventario(models.Model):
    ESTADO = (
        (1, 'Disponible'),
        (2, 'Agotado'),
        (3, 'Por Recibir'),
    )

    producto = models.CharField(max_length=150, blank=True) 
    cantidad = models.FloatField(blank=True) 
    estado = models.PositiveSmallIntegerField(choices=ESTADO)

class Cita(models.Model):
    ESTADO = (
        (1, 'Disponible'),
        (2, 'Agotado'),
        (3, 'Por Recibir'),
    )

    producto = models.CharField(max_length=150, blank=True) 
    cantidad = models.FloatField(blank=True) 
    estado = models.PositiveSmallIntegerField(choices=ESTADO)

class Fecha(models.Model):
    fecha = models.DateField()
    hora = models.TimeField()

    class Meta:
        unique_together = ('fecha', 'hora')

    def __str__(self):
        return f"{self.fecha} {self.hora}"

class Cita(models.Model):
    ESTADO_CHOICES = (
        ('programada', 'Programada'),
        ('completada', 'Completada'),
        ('cancelada', 'Cancelada'),
    )

    MOTIVO_CHOICES = (
        ('protesis', 'Protesis'),
        ('ortodoncia', 'Ortodoncia'),
    )

    paciente = models.ForeignKey(UserProfile, on_delete=models.CASCADE)
    fecha_hora = models.ForeignKey(Fecha, on_delete=models.CASCADE)
    motivo = models.CharField(max_length=20, choices=MOTIVO_CHOICES, default='protesis')
    estado = models.CharField(max_length=20, choices=ESTADO_CHOICES, default='programada')
    asistio = models.BooleanField(default=False)

    def __str__(self):
        return f"Cita de {self.paciente} el {self.fecha_hora}"

    def save(self, *args, **kwargs):
        if self.asistio:
            self.estado = 'completada'
        if self.paciente:
            self.numero = self.paciente 
        super().save(*args, **kwargs)
