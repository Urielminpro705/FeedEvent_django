from django.db import models

# Create your models here.
class Usuario(models.Model):
    nombre = models.CharField("Nombre del usuario", max_length=50, null=False)
    correo = models.CharField("Correo electronico", max_length=50, null=False)
    password = models.CharField("Contraseña del usuario", max_length=30, null=False)
    carrera = models.CharField("Carrera del usuario", max_length=50, default="")
    admin = models.BooleanField("Es cuenta de adminsitrador", default=False)
    superUser = models.BooleanField("Es cuenta de Super usuario", default=False)

    def __str__(self):
        return f'Usuario: {self.nombre}'
    
    @property
    def is_super_user(self):
        return self.superUser
    
    @property
    def is_admin(self):
        return self.admin


class UserManager():
    nombre = 00000