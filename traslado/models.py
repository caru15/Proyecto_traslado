from django.db import models
from django.utils import timezone
from pacientes.models import Paciente
from usuario.models import Usuario,UsuarioRol

class Traslado(models.Model):

    TIPOS_TRASLADO = [
        ('SIMPLE', 'Simple'),
        ('ARM', 'ARM '),
        ('CODIGO_ROJO', 'Código Rojo'),
    ]
    SUBTIPO_TRASLADOS = [
        ('ESTUDIO','Estudio'),
        ('DERIVACION','Derivacion'),
        ('INTERCONSULTA','Interconsulta'),
        ('DOMICILIO','Domicilio')
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
    usuario = models.ForeignKey(
        'usuario.Usuario',
        on_delete= models.PROTECT,#si intentas borrar un Usuario que tiene traslados asociados, no te dejará.
        related_name='traslados_solicitados'#dándole un nombre fácil (traslados_solicitados) para consultar esos datos desde el perfil del usuario
       # Ejemplo de uso en el código:
        #el_usuario = Usuario.objects.get(id=1)
        #todos_sus_traslados = el_usuario.traslados_solicitados.all()
    )
    chofer =models.ForeignKey(
        'usuario.Usuario',
        on_delete= models.PROTECT,
        related_name='traslados_chofer',
        null= True,
        blank=True
    )
    
    enfermeria = models.ForeignKey(
        'usuario.Usuario',
        on_delete=models.PROTECT,
        related_name='traslados_enfermeria',
        null=True,
        blank=True
    )
    tipo = models.CharField(
        max_length=20,
        choices=TIPOS_TRASLADO,
        default='SIMPLE'
    )

    origen = models.CharField(max_length=255)
    destino = models.CharField(max_length=255)
    sub_tipo = models.CharField(
        max_length=20,
        choices=SUBTIPO_TRASLADOS,
        default='ESTUDIO'
    )

    estado = models.CharField(
        max_length=20,
        choices=ESTADOS,
        null= True,
        blank= True,
        default='PENDIENTE'
    )
    origen = models.CharField(max_length=255)
    destino = models.CharField(max_length=255)
   
    requiere_medico = models.BooleanField(default=False)
    ambulancia_privada = models.BooleanField(default=False)#si es privada, ya no la cuento en mi sistema
    # ya que por ahora solo va a registrar traslados con la ambulancia del hospital
    turno_fecha = models.DateField(null=True, blank=True)
    turno_hora = models.TimeField(null=True, blank=True)
    fecha_solicitud = models.DateTimeField(default=timezone.now)
    fecha_alta = models.DateTimeField(auto_now_add=True)
    fecha_modificacion = models.DateTimeField(auto_now=True)
    observacion = models.TextField(blank=True, null=True)

    def __str__(self):
        return f"Traslado #{self.id} - {self.paciente} ({self.tipo})"
    
class HsitoriaEstadoTraslado(models.Model):
    traslado =models.ForeignKey(
        Traslado,
        on_delete=models.CASCADE,
        related_name='historial'#si tienes un objeto traslado, puedes ver toda su historia escribiendo traslado.historial.all()
    )  
    usuario = models.ForeignKey(
        'usuario.Usuario',
        on_delete=models.PROTECT
    )

    estado_anterior = models.CharField(
        max_length=20,
        choices=Traslado.ESTADOS
    )

    estado_nuevo = models.CharField(
        max_length=20,
        choices=Traslado.ESTADOS
    )

    fecha = models.DateTimeField(auto_now_add=True)
    motivo = models.CharField(max_length=255, blank=True)

    class Meta:
        ordering = ['-fecha']  #Establece el orden por defecto, cuando muestre el historial
