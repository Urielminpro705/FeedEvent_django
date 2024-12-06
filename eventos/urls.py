from django.urls import path
from . import views

app_name = "eventos"

urlpatterns = [
    path("", views.IndexView.as_view(), name="index"),
    path("panel/", views.PanelView.as_view(), name="panel")
]