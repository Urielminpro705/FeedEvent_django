from django.views.generic.edit import FormView
from django.views import generic, View
from django.http import HttpResponse, Http404, HttpResponseRedirect
from django.shortcuts import redirect
from .models import Usuario
from django.shortcuts import render
from django.urls import reverse

# Create your views here.
class LoginView(View):
    def get(self, request):
        return render(request, "login.html")

    def post(self, request):
        email = request.POST.get("correo")
        password = request.POST.get("pass")
        user = Usuario.objects.filter(correo=email).first()
        if user and password == user.password:
            request.session['feedID'] = user.id
            return redirect('usuarios:profile')
        else:
            return HttpResponseRedirect(f"{reverse('usuarios:login')}?error=1")
        
def RegisterView(request):
    if request.method == "POST":
        nombre = request.POST.get("nombre")
        correo = request.POST.get("correo")
        password = request.POST.get("password")
        carrera = request.POST.get("carrera")

        requerimientos = [nombre, correo, password, carrera]

        for requerimiento in requerimientos:
            if not requerimiento:
                HttpResponse(request, f'El campo "{requerimiento}"')

        Usuario.objects.create(
            
        )

class ProfileView(View):
    def get(self, request):
        return render(request, "profile.html")

class LogoutView(View):
    def get(self, request):
        request.session['feedID'] = None
        return redirect('eventos:index')
