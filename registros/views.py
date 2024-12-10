from django.shortcuts import render, get_object_or_404, redirect
from .models import Registro
from usuarios.models import Usuario
from eventos.models import Evento
from django.http import HttpResponse
from django.urls import reverse

# Create your views here.
def Registros(request):
    usuario_id = request.session.get("feedID")
    usuario = Usuario.objects.filter(id = usuario_id).first()
    eventos = []
    if usuario:
        registros = Registro.objects.filter(idUsuario=usuario)
        eventos = Evento.objects.filter(registro__idUsuario=usuario).order_by("-cuando")
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

        registros = Registro.objects.filter(idUsuario=usuario, idEvento=evento).first()
        if registros:
            return HttpResponse("El usuario ya esta registrado a ese evento", status=409)

        Registro.objects.create(
            idUsuario = usuario,
            idEvento = evento
        )
        return HttpResponse(f"El usuario '{usuario.nombre}' se registro al evento", status=200)
    return redirect(reverse("eventos:evento", args=(evento_id,)))

def Asistencia(request, evento_id):
    evento = get_object_or_404(Evento, pk=evento_id)
    id_usuario = request.session.get("feedID")
    usuario = Usuario.objects.filter(id=id_usuario).first()
    if not usuario:
        return redirect('usuarios:login')
    
    if evento.Usuario != usuario:
        return redirect('eventos:index')
    
    usuarios = Usuario.objects.filter(registro__idEvento=evento)
    asistencias = Registro.objects.filter(idEvento=evento, asistencia=True)
    usuarios_registrados = [asistencia.idUsuario for asistencia in asistencias]
    print(usuarios_registrados)

    if request.method == "POST":
        lista_id = request.POST.dict()

        usuarios_con_asistencia = [int(id or False) for id in lista_id if id != "csrfmiddlewaretoken"]
        for id in usuarios_con_asistencia:
            if id:
                registro = Registro.objects.filter(idUsuario=id, idEvento=evento).first()
                if registro:
                    registro.asistencia = True
                    registro.save()
        
        usuarios_no_asistentes = usuarios.exclude(id__in=usuarios_con_asistencia)
        for usuario_no_asistente in usuarios_no_asistentes:
            registro = Registro.objects.filter(idUsuario=usuario_no_asistente.id, idEvento=evento).first()
            if registro:
                registro.asistencia = False
                registro.save()
        return redirect(reverse("registros:asistencia", args=(evento.id,)))
    return render(request, "asistencia.html", {"usuarios":usuarios, "evento":evento, "usuarios_registrados":usuarios_registrados})