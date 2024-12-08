from django.urls import path
from . import views

app_name = "eventos"

urlpatterns = [
    path("", views.IndexView.as_view(), name="index"),
    path("busqueda/", views.Busqueda, name="busqueda"),
    path("<int:evento_id>/", views.EventoView, name="evento"),
    path("agregar/", views.AgregarEvento, name="agregarEvento"),
    path("panel/", views.Panel, name="panel"),
    path("eliminar/<int:evento_id>", views.EliminarEvento)
]