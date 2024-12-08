from django.views.generic.edit import FormView
from django.views import generic, View
from django.http import HttpResponse, Http404, HttpResponseRedirect
from django.shortcuts import redirect
from .models import Usuario
from django.shortcuts import render

# Create your views here.
class LoginView(View):
    def get(self, request):
        return render(request, "login.html")

    def post(self, request):
        email = request.POST.get("correo")
        password = request.POST.get("pass")
        user = Usuario.objects.filter(correo=email).first()
        if(password == user.password):
            request.session['feedID'] = user.id
            return redirect('usuarios:profile')
        else:
            return redirect('usuarios:login')

class ProfileView(View):
    def get(self, request):
        return render(request, "profile.html")

class LogoutView(View):
    def get():
        
        print('hola')
