from rest_framework import serializers
from .models import Traslado, HsitoriaEstadoTraslado

class TrasladoSerializer(serializers.ModelSerializer):
    class Meta:
        model = Traslado
        fields = [
            'id',
            'paciente',
            'tipo',
            'subtipo',
            'estado',
            'origen',
            'destino',
            'fecha_creacion',
        ]
        read_only_field = ['estado','fecha_creacion']#CON CAMPOS Q no se cambian directamente, se cmbvia con servicios 

class CambioEstadoSerializer(serializers.Serializer):
        nuevo_estado =serializers.CharField()
        motivo = serializers.CharField(required = False, allow_blank = True)

class HistorialEstadoSerializer(serializers.ModelSerializer):#este es de solo lectura
    usuario = serializers.StringRelatedField() #usa el ___strin__() del usuario

    class Meta:
            model = HsitoriaEstadoTraslado
            field = [
                'id',
                'estado_anterior',
                'estado_nuevo',
                'usuario',
                'fecha',
                'motivo',
            ]    

