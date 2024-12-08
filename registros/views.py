from django.shortcuts import render
from django.views import generic
from .models import Registro
from eventos.models import Evento

# Create your views here.
def Registros(request):
    registros = Registro.objects.filter(idUsuario=1)
    eventos = registros.evento_set.order_by("-cuando")
    context = {
        "eventos": eventos
    }
    return render(request, "actividades_inscritas.html",context)