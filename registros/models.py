from django.db import models
from usuarios.models import Usuario
from eventos.models import Evento

# Create your models here.
class Registro(models.Model):
    idUsuario = models.ForeignKey(Usuario, on_delete=models.CASCADE)
    idEvento = models.ForeignKey(Evento, on_delete=models.CASCADE)
    asistencia = models.BooleanField("Asistencia al evento", null=False, blank=False, default=0)