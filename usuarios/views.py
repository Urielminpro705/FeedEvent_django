from django.shortcuts import render
from django.views import generic

# Create your views here.

class LoginView(generic.ListView, ):
    template_name = "login.html"

    def get_queryset(self):
        return
    
    
