from django.db import models
from pacientes.models import Paciente


class Traslado(models.Model):

    TIPOS_TRASLADO = [
        ('SIMPLE', 'Simple'),
        ('ARM', 'ARM '),
        ('CODIGO_ROJO', 'Código Rojo'),
    ]

    ESTADOS = [
        ('PENDIENTE', 'Pendiente'),
        ('AUTORIZADO', 'Autorizado'),
        ('EN_TRASLADO', 'En traslado'),
        ('REALIZADO', 'Realizado'),
        ('CANCELADO', 'Cancelado'),
    ]

    paciente = models.ForeignKey(
        Paciente,
        on_delete=models.CASCADE,
        related_name='traslados'
    )

    tipo = models.CharField(
        max_length=20,
        choices=TIPOS_TRASLADO,
        default='SIMPLE'
    )

    origen = models.CharField(max_length=255)
    destino = models.CharField(max_length=255)

    estado = models.CharField(
        max_length=20,
        choices=ESTADOS,
        default='PENDIENTE'
    )

    requiere_medico = models.BooleanField(default=False)
    ambulancia_privada = models.BooleanField(default=False)

    fecha_creacion = models.DateTimeField(auto_now_add=True)

    observacion = models.TextField(blank=True, null=True)

    def __str__(self):
        return f"Traslado #{self.id} - {self.paciente} ({self.tipo})"