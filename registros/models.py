from django.db import models
from usuarios.models import Usuario
from eventos.models import Evento

# Create your models here.
class Registros(models.Model):
    idUsuario = models.ForeignKey(Usuario, on_delete=models.CASCADE)
    idEvento = models.ForeignKey(Evento, on_delete=models.CASCADE)