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
    if request.method == 'POST':
        nombre = request.POST.get("nombre")
        correo = request.POST.get("correo")
        password = request.POST.get("password")
        password2 = request.POST.get("password2")
        carrera = request.POST.get("carrera")

        requerimientos = [
            ["Nombre", nombre],
            ["correo", correo], 
            ["password", password], 
            ["confirmar contraseñas", password2], 
            ["carrera", carrera]
        ]

        usuario_correo = Usuario.objects.filter(correo=correo).first()

        if usuario_correo:
            return render(request,"register.html", {"mensaje": "Ya existe un usuario con ese correo"})

        for campo, valor in requerimientos:
            if not valor:
                # return HttpResponse(f'El campo "{campo}" es obligatorio', status=400)
                return render(request, "register.html", {"mensaje": f'El campo "{campo}" es obligatorio'})

        if password != password2:
            # return HttpResponse("Las contraseñas no coinciden", status=400)
            return render(request, "register.html", {"mensaje": "Las contraseñas no coinciden"})

        Usuario.objects.create(
            nombre = nombre,
            correo = correo,
            password = password,
            carrera = carrera
        )

        return render(request, "login.html")
    else:
        return render(request, "register.html")

class ProfileView(View):
    def get(self, request):
        return render(request, "profile.html")

class LogoutView(View):
    def get(self, request):
        request.session['feedID'] = None
        return redirect('eventos:index')
