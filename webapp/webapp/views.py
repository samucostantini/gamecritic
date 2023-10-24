from telnetlib import *
from telnetlib import LOGOUT
from django.http import HttpResponse
from django.shortcuts import render, redirect
from django.urls import reverse_lazy
from .forms import *
from django.views.generic.edit import CreateView
from django.contrib.auth.mixins import PermissionRequiredMixin
from django.contrib.auth.views import LoginView
from django.contrib.auth.models import Group
from gestione.models import *


def home(request):
    games=Game.objects.filter()
    
    #return render(request, template_name="home.html")
    return render(request, "home.html",{'games' : games , 'i':0})

class UserCreateView(CreateView):
    form_class=CreateUser
    template_name="user_register.html"
    success_url= reverse_lazy("login")
    

#after correct login user is redirect to viewPage in Gestione
class CustomLoginView(LoginView):
    def get_success_url(self):
        return reverse_lazy('gestione:viewPage')  

def logout_view(request):
    LOGOUT(request)
    return redirect('home')
#----------------------------#

class PlayerCreateView(CreateView):
    #form_class = UserCreationForm
    form_class = CreatePlayer
    template_name = "user_create.html"
    #template_name = "playerRegCrispy.html"
    success_url = reverse_lazy("login")

class PublisherCreateView(CreateView):
    form_class = CreatePublisher
    #template_name = "playerRegistrate.html"
    #template_name = "playerRegCrispy.html"
    template_name = "user_create.html"
    success_url = reverse_lazy("login")
    



