"""
URL configuration for webapp project.

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/4.2/topics/http/urls/
Examples:
Function views
    1. Add an import:  from my_app import views
    2. Add a URL to urlpatterns:  path('', views.home, name='home')
Class-based views
    1. Add an import:  from other_app.views import Home
    2. Add a URL to urlpatterns:  path('', Home.as_view(), name='home')
Including another URLconf
    1. Import the include() function: from django.urls import include, path
    2. Add a URL to urlpatterns:  path('blog/', include('blog.urls'))
"""
from django.contrib import admin
from django.urls import include, path
from django.contrib.auth import views as auth_views
from . import views
from .views import *
from .forms import *

#con registerP e registerPu, registro un utente che viene assegnato a un gruppo player o publisher

urlpatterns = [
    path('admin/', admin.site.urls),
    path('',views.home, name="home"),
    path("register/", UserCreateView.as_view(), name="register"),
    path("login/",CustomLoginView.as_view(), name="login"),
    
    path("registerP/", PlayerCreateView.as_view(), name="registerP"),
    path("registerPu/", PublisherCreateView.as_view(), name="registerPu"),
    path('gestione/',include('gestione.urls')),
    path("logout/", auth_views.LogoutView.as_view(), name="logout"),

    
]