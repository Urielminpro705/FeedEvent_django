from django.http import HttpResponse
from django.shortcuts import render
from django.views import generic
from .models import Evento
from django.shortcuts import get_list_or_404, get_object_or_404, redirect
from django.utils import timezone

class IndexView(generic.ListView):
    template_name = "index.html"
    context_object_name = "eventos"

    def get_queryset(self):
        return Evento.objects.all()

def busqueda(request):
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

class PanelView(generic.ListView):
    template_name = "panel.html"
    context_object_name = "eventos_del_usuario"

    def get_queryset(self):
        return Evento.objects.all()
    
def EventoView(request, evento_id):
    evento = get_object_or_404(Evento, pk=evento_id)
    context = {"evento":evento}
    return render(request, "publicacion.html", context)

def EliminarEvento(request, evento_id):
    evento = get_object_or_404(Evento, pk=evento_id)
    return redirect("eventos:panel")

def AgregarEvento(request):
    if request.method =='POST':
        titulo = request.POST.get("titulo")
        descr = request.POST.get("desc")
        cuando = request.POST.get("cuando")
        horaInicio = request.POST.get("horaInicio")
        horaFin = request.POST.get("horaFin")
        fechaCreacion = timezone.now()
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
            fechaCreacion=fechaCreacion
        )
        return HttpResponse("OK", status=200)
    return HttpResponse("Método no permitido", status=405)