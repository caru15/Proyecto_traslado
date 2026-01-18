from django.db import models

class Paciente(models.Model):
    
    # id = models.AutoField(primary_key=True)

    apellido = models.CharField(max_length=255)
    nombre = models.CharField(max_length=255)
    dni = models.IntegerField(max_length=20, unique=True) 
    peso = models.FloatField(null=True, blank=True)
    obrasocial_id = models.IntegerField() 
    observacion = models.TextField(blank=True, null=True)
    def __str__(self):
        return f"{self.apellido}, {self.nombre}"
    #class Meta:
       # db_table = 'paciente'
