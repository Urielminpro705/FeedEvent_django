from django.shortcuts import render
from django.views import generic
from .models import Registro
from eventos.models import Evento

# Create your views here.
def Registros(request):
    usuario = request.session.get("CURRENT_USER")
    eventos = []
    if usuario:
        registros = Registro.objects.filter(idUsuario=usuario)
        eventos = registros.evento_set.order_by("-cuando")
    context = {
        "eventos": eventos
    }
    return render(request, "actividades_inscritas.html",context)