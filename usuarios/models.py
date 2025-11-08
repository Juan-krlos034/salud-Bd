
from django.db import models

class Usuario(models.Model):
    id_usuario = models.AutoField(primary_key=True)
    nombre = models.CharField(max_length=100)
    apellidos = models.CharField(max_length=100)
    documento = models.CharField(max_length=50, unique=True)
    fecha_nacimiento = models.DateField(null=True)
    correo = models.CharField(max_length=100, unique=True)
    telefono = models.CharField(max_length=20, null=True)
    contrasena = models.CharField(max_length=100)
    rol = models.CharField(max_length=20)

    class Meta:
        managed = False
        db_table = 'Usuario'
