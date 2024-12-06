from django.db import models

# Create your models here.
class Usuario(models.Model):
    nombre = models.CharField("Nombre del usuario", max_length=50)
    correo = models.CharField("Correo electronico", max_length=50)
    password = models.CharField("Contraseña del usuario", max_length=10)
    caarrera = models.CharField("Carrera del usuario", max_length=20)
    superUser = models.BooleanField("Es cuenta de adminsitrador", default=False)