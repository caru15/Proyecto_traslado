from django.shortcuts import render
from rest_framework import viewsets, status
from rest_framework.decorators import action
from rest_framework. response import Response
from .models import Traslado, HsitoriaEstadoTraslado
from .serializers import (
    TrasladoSerializer,
    CambioEstadoSerializer,
    HistorialEstadoSerializer
)
from traslado.servicios.estado_traslado_service import EstadoTrasladoService

class TrasladoViewSet(viewsets.ModelViewSet):
    queryset = Traslado.objects.all()
    serializer_class = TrasladoSerializer

@action(detail=True, methods=['post'], url_path='cambiar-estado')
    def cambiar_estado(self, request, pk=None):
        traslado = self.get_object()
        serializer = CambioEstadoSerializer(data=request.data)
        serializer.is_valid(raise_exception=True)

        EstadoTrasladoService.cambiar_estado(
            traslado=traslado,
            nuevo_estado=serializer.validated_data.get('nuevo_estado'),
            motivo=serializer.validated_data.get('motivo', ''),
            usuario=request.user
        )

        return Response(
            TrasladoSerializer(traslado).data,
            status=status.HTTP_200_OK
        )
