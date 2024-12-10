from django.http import HttpResponse
from django.shortcuts import render
from django.views import generic
from .models import Evento
from usuarios.models import Usuario
from registros.models import Registro
from django.shortcuts import get_list_or_404, get_object_or_404, redirect
from django.utils import timezone
from datetime import datetime

class IndexView(generic.ListView):
    template_name = "index.html"
    context_object_name = "eventos"

    def get_queryset(self):
        return Evento.objects.all()

def Busqueda(request):
    solidarios = request.GET.get("solidarios", 0)
    culturales = request.GET.get("culturales", 0)
    deportivos = request.GET.get("deportivos", 0)
    titulo = request.GET.get("titulo", "")
    eventos = Evento.objects.filter(
        solidarios__gte=solidarios, 
        deportivos__gte=deportivos, 
        culturales__gte=culturales,
        titulo__icontains = titulo
    )

    context = {"eventos":eventos}
    return render(request, "index.html", context)

def Panel(request):
    id_usuario = request.session.get("feedID")
    usuario = Usuario.objects.filter(id=id_usuario).first()
    if not usuario:
        return redirect('usuarios:login')
    
    if not usuario.admin:
        return redirect('eventos:index')


    ahora = timezone.localtime().now()
    eventos = Evento.objects.filter(Usuario=usuario)
    eventos_pasados = []
    eventos_actuales = []

    for evento in eventos:
        fecha_hora_evento = datetime.combine(evento.cuando, evento.horaInicio)

        if fecha_hora_evento <= ahora:
            eventos_pasados.append(evento)
        else:
            eventos_actuales.append(evento)

    context = {
        "eventos_pasados": eventos_pasados,
        "eventos_actuales": eventos_actuales,
    }
    return render(request, "panel.html", context)

def EventoView(request, evento_id):
    evento = get_object_or_404(Evento, pk=evento_id)
    id_usuario = request.session.get("feedID")
    usuario = Usuario.objects.filter(id=id_usuario).first()

    if usuario:
        inscripcion = Registro.objects.filter(idUsuario=usuario, idEvento=evento).first()
        if inscripcion:
            estaInscrito = True
        else:
            estaInscrito = False
    else:
        estaInscrito = False
    context = {
        "evento": evento,
        "estaInscrito": estaInscrito 
    }
    return render(request, "publicacion.html", context)

def EliminarEvento(request, evento_id):
    id_usuario = request.session.get("feedID")
    usuario = Usuario.objects.filter(id=id_usuario).first()
    if not usuario:
        return redirect("eventos:index")
    if not usuario.admin:
        return redirect("eventos:index")

    evento = get_object_or_404(Evento, pk=evento_id)
    if evento.Usuario == usuario:
        evento.delete()
    return redirect("eventos:panel")

def AgregarEvento(request):
    id_usuario = request.session.get("feedID")
    usuario = Usuario.objects.filter(id=id_usuario).first()
    if not usuario:
        return HttpResponse("No hay una sesion iniciada", status=403)
    if not usuario.admin:
        return HttpResponse("El usuario no tiene los permisos", status=403)
    if request.method =='POST':
        titulo = request.POST.get("titulo")
        descr = request.POST.get("desc")
        cuando = request.POST.get("cuando")
        horaInicio = request.POST.get("horaInicio")
        horaFin = request.POST.get("horaFin")
        fechaCreacion = timezone.localtime().now()
        imagen = request.FILES.get("imagen")
        requisitos = request.POST.get("requisitos")

        if not imagen:
            imagen = "imagenes_eventos/imagen_default_evento.webp"
        if not requisitos:
            requisitos = "Sin requisitos"
        solidarios = int(request.POST.get("solid") or 0)
        culturales = int(request.POST.get("cult") or 0)
        deportivos = int(request.POST.get("deport") or 0)

        parametros_obligatorios = [
            ["titulo", titulo],
            ["descr", descr],
            ["cuando", cuando],
            ["horaInicio", horaInicio],
            ["horaFin", horaFin]
        ]

        for campo, valor in parametros_obligatorios:
            if not valor:
                return HttpResponse(f"El campo {campo} es obligatorio", status=400)

        evento = Evento.objects.create(
            titulo=titulo,
            descr=descr,
            requisitos=requisitos,
            cuando=cuando,
            solidarios=solidarios,
            culturales=culturales,
            deportivos=deportivos,
            imagen=imagen,
            horaInicio=horaInicio,
            horaFin=horaFin,
            Usuario = usuario,
            fechaCreacion=fechaCreacion
        )
        return HttpResponse("Evento creado correctamente", status=200)
    return HttpResponse("Método no permitido", status=405)

def ActualizarEvento(request, evento_id):
    id_usuario = request.session.get("feedID")
    usuario = Usuario.objects.filter(id=id_usuario).first()
    if not usuario:
        return HttpResponse("No hay una sesion iniciada", status=403)
    if not usuario.admin:
        return HttpResponse("El usuario no tiene los permisos", status=403)
    evento = get_object_or_404(Evento, pk=evento_id)
    if evento.Usuario != usuario:
        return HttpResponse("El usuario no es dueño del evento", status=403)
    if request.method == 'POST':
        imagen = request.FILES.get("imagen")
        descr = request.POST.get("desc")

        if not imagen:
            imagen = evento.imagen
        
        evento.imagen = imagen
        evento.descr = descr
        evento.save()
        return HttpResponse("Evento actualizado correctamente", status=200)
    return HttpResponse("Método no permitido", status=405)