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
    def _es_codigo_rojo(cls, traslado:Traslado)-> bool:
        return traslado.tipo == 'CODIGO_ROJO'
    
    
    @classmethod
    def _es_admin(cls, usuario) -> bool:
        return usuario.roles.filter(nombre='ADMINISTRATIVO').exists()

    @classmethod
    def _validar_rol(cls, usuario, estado_actual, nuevo_estado):
        roles = set(usuario.roles.values_list('nombre', flat=True))

        # ADMINISTRATIVO: puede todo
        if 'ADMINISTRATIVO' in roles:
            return

        # ENFERMERIA
        if 'ENFERMERIA' in roles:
            if estado_actual == 'PENDIENTE' and nuevo_estado == 'AUTORIZADO':
                return
            if estado_actual == 'AUTORIZADO' and nuevo_estado == 'EN_TRASLADO':
                return
            if estado_actual == 'EN_TRASLADO' and nuevo_estado in ['REALIZADO', 'CANCELADO']:
                return

        # CHOFER
        if 'CHOFER' in roles:
            if estado_actual == 'EN_TRASLADO' and nuevo_estado in ['REALIZADO', 'CANCELADO']:
                return

        raise PermissionError(
            f"Rol sin permisos para cambiar de {estado_actual} a {nuevo_estado}"
        )

    @classmethod
    @transaction.atomic
    def cambiar_estado(
        cls,
        *,
        traslado: Traslado,
        nuevo_estado: str | None,
        usuario,
        motivo: str = ""
    ):
        # 🔴 Código Rojo: no hay flujo de estados
        if cls._es_codigo_rojo(traslado):
            HistorialEstadoTraslado.objects.create(
                traslado=traslado,
                usuario=usuario,
                estado_anterior=traslado.estado,
                estado_nuevo=nuevo_estado,
                motivo=motivo or "Traslado Código Rojo"
            )
            traslado.estado = nuevo_estado
            traslado.save(update_fields=['estado'])
            return

        estado_actual = traslado.estado

        # 1️⃣ Validar transición lógica
        if nuevo_estado not in cls.TRANSICIONES_VALIDAS.get(estado_actual, []):
            raise ValueError(
                f"Transición inválida: {estado_actual} → {nuevo_estado}"
            )

        # 2️⃣ Validar rol
        cls._validar_rol(usuario, estado_actual, nuevo_estado)

        # 3️⃣ Historial
        HistorialEstadoTraslado.objects.create(
            traslado=traslado,
            usuario=usuario,
            estado_anterior=estado_actual,
            estado_nuevo=nuevo_estado,
            motivo=motivo
        )

        # 4️⃣ Cambio de estado
        traslado.estado = nuevo_estado
        traslado.save(update_fields=['estado'])