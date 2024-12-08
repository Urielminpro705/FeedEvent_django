from django.shortcuts import render, get_object_or_404, redirect
from .models import Registro
from usuarios.models import Usuario
from eventos.models import Evento
from django.http import HttpResponse
from django.urls import reverse

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

def NuevoRegistro(request, evento_id):
    if request.method == 'POST':
        id_evento = evento_id
        id_usuario = request.POST.get("id_usuario")

        requerimientos = [
            ["id_evento", id_evento],
            ["id_usuario", id_usuario]
        ]

        for campo, valor in requerimientos:
            if not valor:
                return HttpResponse(f"El campo {campo} es obligatorio", status=400)
        
        usuario = get_object_or_404(Usuario, pk=id_usuario)
        evento = get_object_or_404(Evento, pk=id_evento)

        Registro.objects.create(
            idUsuario = usuario,
            idEvento = evento
        )
        return HttpResponse(f"El usuario '{usuario.nombre}' se registro al evento", status=200)
    return redirect(reverse("eventos:evento", args=(evento_id,)))