
import random
from django.shortcuts import render, redirect
from django.contrib.auth.decorators import login_required
from django.urls import reverse_lazy

from .models import *
from .views import *

from .utility import *
from .forms import *

from django.contrib.auth.models import User

# Create your views here.
def is_group_publisher_member(user):
    return user.groups.filter(name='Publisher').exists()

def is_group_player_member(user):
    return user.groups.filter(name='Player').exists()

@login_required
def player_home(request):
     if request.user.groups.filter(name='Player').exists():
        player=Player.objects.get(user=request.user)
        games = list(player.games.all())
        if len(games) >= 2:
            random_games = random.sample(games, 2)
        else:
            random_games = games
        
        return render(request, "home_player.html",{'games':random_games})

def player_registration2(request):
    if request.method == 'POST':
        name = request.POST.get('name')
        surname = request.POST.get('surname')
        pict = request.FILES['pict']
        age=request.POST.get('age')
        console=request.POST.get('console')
        country = request.POST.get('country')

        # Recupera l'utente autenticato
        user = request.user

        # Crea il profilo dell'editore
        player = Player(user=user, name=name,surname=surname, age=age, pict=pict,console=console, country=country)
        player.save()

        return redirect("/gestione/playerHome") 
    return render(request, 'playerRegistration.html')  
     
#-----------------player registration----------------------#
@login_required
def player_registration(request):
    if request.method == 'POST':
        name = request.POST.get('name')
        surname = request.POST.get('surname')
        pict = request.FILES['pict']
        age=request.POST.get('age')
        console=request.POST.get('console')
        country = request.POST.get('country')

        # Recupera l'utente autenticato
        user = request.user

        # Crea il profilo dell'editore
        player = Player(user=user, name=name,surname=surname, age=age, pict=pict,console=console, country=country)
        player.save()
        registrazione_avvenuta = True  # Indica che la registrazione è andata a buon fine
        return render(request, 'playerRegistration.html', {'registrazione_avvenuta': registrazione_avvenuta})

    return render(request, 'playerRegistration.html')  
    

@login_required
@user_passes_test(is_group_player_member)
def player_profile(request):
    if request.method == 'POST':
        game_id_del = request.POST.get('game_id_remove')
        game = Game.objects.get(id=game_id_del)
        request.user.player.games.remove(game)
        return redirect('/gestione/playerProfile')
    
    player = Player.objects.get(user=request.user)
    return render(request, 'playerProfile.html', {'player': player})

"""
def game_recommended(request):
    #prendo tutti i player che hanno aggiunto un gioco uguale a quello che ho aggiunto io come player
    other_player=Player.objects.exclude(user = request.user)
    player=Player.objects.get(user=request.user)
    game_list=Game.objects.all()
    list_g=[]
    
    for p in other_player:
"""       
    
    
    
    
    
@login_required
@user_passes_test(is_group_player_member)  
def game_recommended(request):
    # Prendo tutti i player che hanno almeno un gioco in comune con il giocatore corrente
    player = Player.objects.get(user=request.user)
    user_games = set(player.games.all())
    other_player=Player.objects.exclude(user=request.user)


    suggested_games_weights = {}

    for p in other_player:
        other_games = set(p.games.all())
        common_games = user_games.intersection(other_games)

        if common_games:
            for game in other_games - user_games:
                if game in suggested_games_weights:
                    suggested_games_weights[game] += 1
                else:
                    suggested_games_weights[game] = 1

    
    suggested_games = sorted(suggested_games_weights.keys(), key=suggested_games_weights.get, reverse=True)[:2]
    
    
    
    rec_game=get_recommended_games_by_category_added(user_games)
    
    return render(request, 'gameRecom.html',{'games':suggested_games,'rec_game':rec_game})
     
       
       
def my_games(request):
    player=Player.objects.get(user=request.user)
    games=player.games
    
    return render(request,"myGames.html",{'games':games})

def specSearch(request):
    games=Game.objects.all()
    if request.method == 'POST':
        category=request.POST.get('category')
        category2=request.POST.get('category2')
        price_min=request.POST.get('price_min')
        price_max=request.POST.get('price_max')
        console=request.POST.get('console')
        rating=request.POST.get('rating')  #from 1 to 5
     
        sugg_games=Game.objects.all()
        
        for g in sugg_games:
            if g.category != category or g.category != category2:
                g.delete
            if g.price < price_min and g.price > price_max:
                g.delete    

       
        

       
        return render(request, 'risultati_ricerca.html', {'games': games})

    # Se la richiesta non è di tipo POST, potresti fare qualcos'altro,
    # come visualizzare la pagina di ricerca.
    return render(request, 'specSearch.html',{'games':games})
    