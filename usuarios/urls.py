from django.urls import path
from . import views

app_name = "usuarios"

urlpatterns = [
    path("", views.LoginView.as_view(), name="login"),
    path("profile/", views.ProfileView.as_view(), name="profile"),
]