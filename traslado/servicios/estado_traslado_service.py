from django.db import transaction
from traslado.models import Traslado, HsitoriaEstadoTraslado

class EstadoTrasladoService:
    TRANSICIONES_VALIDAS = {
            'PENDIENTE': ['AUTORIZADO', 'CANCELADO'],
            'AUTORIZADO': ['EN_TRASLADO','CANCELADO'],
            'EN_TRASLADO': ['REALIZADO','CANCELADO'],
            'REALIZADO': [],
            'CANCELADO':[],
    }
    @classmethod
    @transaction.atomic
    def cambiar_estado( #cambiar_estado(traslado=t1, nuevo_estado='AUTORIZADO', usuario=user--este es el formato de los parametrsod ede la funcion
        cls,
        *,
        traslado: Traslado,
        nuevo_estado: str,
        usuario,
        motivo: str = ""
    ):
        estado_actual = traslado.estado

        # 1️⃣ Validar transición
        if nuevo_estado not in cls.TRANSICIONES_VALIDAS.get(estado_actual, []):
            raise ValueError(
                f"No se puede cambiar el estado de {estado_actual} a {nuevo_estado}"
            )

        # 2️⃣ Guardar historial
        HistorialEstadoTraslado.objects.create(
            traslado=traslado,
            usuario=usuario,
            estado_anterior=estado_actual,
            estado_nuevo=nuevo_estado,
            motivo=motivo
        )

        # 3️⃣ Cambiar estado
        traslado.estado = nuevo_estado
        traslado.save(update_fields=['estado'])
