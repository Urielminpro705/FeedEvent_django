from django.urls import path
from . import views

app_name = "registros"

urlpatterns = [
    path("", views.Registros, name="registros"),
    path("registro/<int:evento_id>", views.NuevoRegistro, name="nuevoRegistro"),
    path("asistencia/<int:evento_id>", views.Asistencia, name="asistencia")
]