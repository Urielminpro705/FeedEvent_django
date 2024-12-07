from django.urls import path
from . import views

app_name = "eventos"

urlpatterns = [
    path("", views.IndexView.as_view(), name="index"),
    path("busqueda/", views.busqueda, name="busqueda"),
    path("<int:evento_id>/", views.EventoView, name="evento"),
    path("agregar/", views.AgregarEvento, name="agregarEvento"),
    path("panel/", views.PanelView.as_view(), name="panel")
]