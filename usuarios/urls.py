from django.urls import path
from . import views

app_name = "usuarios"

urlpatterns = [
    path("", views.LoginView.as_view(), name="login"),
    path("profile/", views.ProfileView.as_view(), name="profile"),
    path("logout/", views.LogoutView.as_view(), name="logout"),
    path("register/", views.RegisterView, name="register"),
    path("grant-superuser", views.GrantSuperUserView.as_view(), name="grant_superuser")
]