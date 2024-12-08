from django.db import models
from usuarios.models import Usuario
from django.templatetags import static
import os

# Create your models here.
class Evento(models.Model):
    titulo = models.CharField("Titulo del evento", max_length = 100, null=False, blank=False)
    descr = models.CharField("Descripcion del evento", max_length = 200, null=False, blank=False)
    requisitos = models.CharField("Requisitos para el evento", max_length = 400, default="Sin requisitos")
    cuando = models.DateField("Fecha del evento", null=False, blank=False)
    solidarios = models.IntegerField("Creditos solidarios", default=0)
    culturales = models.IntegerField("Creditos culturales", default=0)
    deportivos = models.IntegerField("Creditos deportivos", default=0)
    fechaCreacion = models.DateTimeField("Fecha y hora de creacion", null=False, blank=False)
    imagen = models.ImageField(upload_to="imagenes_eventos/", default="imagenes_eventos/imagen_default_evento.webp")
    # idUsuario = models.ForeignKey(Usuario, on_delete=models.PROTECT)
    horaInicio = models.TimeField("Hora de inicio", max_length=10, null=False, blank=False)
    horaFin = models.TimeField("Hora de finalizacion", max_length=10, null=False, blank=False)

    def __str__(self):
        return self.titulo
    
    def delete(self, *args, **kwargs):
        if self.imagen:
            if os.path.isfile(self.imagen.path):
                os.remove(self.imagen.path)
        
        super().delete(*args, **kwargs)