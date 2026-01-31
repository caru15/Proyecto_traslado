from django.db import models
from django.contrib.auth.models import AbstractBaseUser, PermissionsMixin, BaseUserManager

# 1. El Manager: Este se encarga de la lógica de creación de usuarios
class UsuarioManager(BaseUserManager):
    def create_user(self, username, nombre, password=None, **extra_fields):
        if not username:
            raise ValueError('El usuario debe tener un username')
        
        # Normaliza el email si existe
        email = self.normalize_email(extra_fields.get('email'))
        if email:
            extra_fields['email'] = email

        user = self.model(username=username, nombre=nombre, **extra_fields)
        user.set_password(password)
        user.save(using=self._db)
        return user

    def create_superuser(self, username, nombre, password=None, **extra_fields):
        extra_fields.setdefault('is_staff', True)
        extra_fields.setdefault('is_superuser', True)
        extra_fields.setdefault('activo', True)

        if extra_fields.get('is_staff') is not True:
            raise ValueError('Superuser debe tener is_staff=True.')
        if extra_fields.get('is_superuser') is not True:
            raise ValueError('Superuser debe tener is_superuser=True.')

        return self.create_user(username, nombre, password, **extra_fields)

class Rol(models.Model):
    nombre = models.CharField(max_length=100, unique=True)
    descripcion = models.CharField(max_length=150, blank=True)
    
    def __str__(self):
        return self.nombre
    
    class Meta:
        db_table = 'rol'

class Usuario(AbstractBaseUser, PermissionsMixin):
    nombre = models.CharField(max_length=150)
    username = models.CharField(max_length=100, unique=True)
    email = models.EmailField(unique=True, null=True, blank=True)
    activo = models.BooleanField(default=True)
    fecha_alta = models.DateTimeField(auto_now_add=True)
    
    # --- CAMPOS OBLIGATORIOS PARA DJANGO ADMIN ---
    is_staff = models.BooleanField(default=False) 
    # (is_superuser ya lo hereda de PermissionsMixin)

    # --- CONFIGURACIÓN DEL MANAGER ---
    objects = UsuarioManager()

    USERNAME_FIELD = 'username'
    REQUIRED_FIELDS = ['nombre'] # Campos que pide createsuperuser aparte de username y password

    def __str__(self):
        return f"{self.nombre}-{self.username}"
    
    class Meta:
        db_table = 'usuario'

class UsuarioRol(models.Model):
    usuario = models.ForeignKey(Usuario, on_delete=models.CASCADE)
    rol = models.ForeignKey(Rol, on_delete=models.PROTECT)

    class Meta:
        db_table = 'usuario_rol'
        unique_together = ('usuario', 'rol')