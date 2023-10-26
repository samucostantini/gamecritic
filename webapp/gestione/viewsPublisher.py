from django.shortcuts import render, redirect
from django.contrib.auth.decorators import login_required
from django.urls import reverse_lazy

from .models import *
from .viewsPlayer import *
from .views import *
from .utility import *

from django.contrib.auth.models import User
from django.contrib.auth.decorators import user_passes_test
from django.http import HttpResponse
from reportlab.pdfgen import canvas

# Create your views here.
def is_group_publisher_member(user):
    return user.groups.filter(name='Publisher').exists()

@login_required
def publisher_registration(request):
    if request.method == 'POST':
        name = request.POST.get('name')
        website = request.POST.get('website')
        pict = request.FILES['pict']

        # Recupera l'utente autenticato
        user = request.user

        # Crea il profilo dell'editore
        publisher = Publisher(user=user, name=name, website=website, pict=pict)
        publisher.save()
        
        registrazione_avvenuta = True  # Indica che la registrazione è andata a buon fine
        return render(request, 'publisherRegistration.html', {'registrazione_avvenuta': registrazione_avvenuta})

    return render(request, 'publisherRegistration.html')  # Assumi che il tuo template si chiami 'registration.html'

@login_required
def edit_publisher_profile(request):
    user = request.user
    publisher = Publisher.objects.get(user=user)

    if request.method == 'POST':
        name = request.POST.get('name')
        website = request.POST.get('website')
        pict = request.FILES.get('pict')

        # Aggiorna i campi del profilo dell'editore
        publisher.name = name
        publisher.website = website
        if pict:
            publisher.pict = pict
        publisher.save()
        
        registrazione_avvenuta = True  # Indica che la modifica è andata a buon fine
        return render(request, 'editPublisherProfile.html', {'registrazione_avvenuta': registrazione_avvenuta})

    return render(request, 'editPublisherProfile.html', {'publisher': publisher})

@user_passes_test(is_group_publisher_member)
def publisher_home(request):
     if request.user.groups.filter(name='Publisher').exists():
        publisher=Publisher.objects.get(user=request.user)
        games = Game.objects.filter(publisher=publisher)
        return render(request,"home_publisher.html",{'games': games, 'publisher':publisher})


def publisher_profile(request,publisher_id):
    publisher = Publisher.objects.get(id=publisher_id)
    games=Game.objects.filter(publisher=publisher)
    return render(request, 'publisherProfile.html', {'publisher': publisher, 'games':games})



@login_required
def show_publisher_game(request):
    games = Game.objects.filter(publisher=Publisher.objects.get(user=request.user))
    return render(request, 'gamePub.html', {'games': games})

def show_game_stat(request, game_id):
    game=Game.objects.get(pk=game_id)
    reviews=Review.objects.filter(game=game)
    return render(request,'showgameReview.html',{'reviews':reviews})

@login_required
@user_passes_test(is_group_publisher_member)
def show_allGames_stat(request):
    pub=Publisher.objects.get(user=request.user)
    games=Game.objects.filter(publisher=pub)
    
    games_added={}
    
    for game in games:
        n=Player.objects.filter(games=game)
        games_added[game]=len(n)
        
    games_rating={}
    
    for game in games:
        rating=(game.average_gameplay_rating+game.average_music_rating+game.average_performance_rating+game.average_plot_rating)/4
        games_rating[game]=rating

    return render(request,'analyticsAll.html',{'games_added':games_added, 'games_rating':games_rating})
    



