from django.shortcuts import render
from django.views import generic
from .models import Evento

# Create your views here.
class IndexView(generic.ListView):
    template_name = "index.html"
    context_object_name = "lista_todos_los_eventos"

    def get_queryset(self):
        return Evento.objects.all()