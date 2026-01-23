from django.contrib import admin
from .models import Paciente, ObraSocial

admin.site.register(Paciente) #sto significa quiero administrar pacientes desde el panel de administracion
admin.site.register(ObraSocial)