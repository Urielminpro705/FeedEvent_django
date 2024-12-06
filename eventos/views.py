from django.shortcuts import render
from django.views import generic
from .models import Evento

# Create your views here.
class IndexView(generic.ListView):
    template_name = "index.html"
    context_object_name = "lista_todos_los_eventos"

    def get_queryset(self):
        return Evento.objects.all()

class PanelView(generic.ListView):
    template_name = "panel.html"
    context_object_name = "eventos_del_usuario"

    def get_queryset(self):
        return Evento.objects.filter(idUsuario = 1)