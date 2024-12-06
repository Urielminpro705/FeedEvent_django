from django.db import models
from usuarios.models import Usuario

# Create your models here.
class Evento(models.Model):
    titulo = models.CharField("Titulo del evento", max_length = 100)
    descr = models.CharField("Descripcion del evento", max_length = 200)
    cuando = models.DateField("Fecha del evento")
    solidarios = models.IntegerField("Creditos solidarios")
    culturales = models.IntegerField("Creditos culturales")
    deportivos = models.IntegerField("Creditos deportivos")
    fechaCreacion = models.DateTimeField("Fecha y hora de creacion")
    imagen = models.ImageField(upload_to="imagenes_eventos/")
    idUsuario = models.ForeignKey(Usuario, on_delete=models.PROTECT)
    horaInicio = models.CharField("Hora de inicio", max_length=10)
    horaFin = models.CharField("Hora de finalizacion", max_length=10)

    def __str__(self):
        return self.titulo