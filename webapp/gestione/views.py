from django.db import IntegrityError
from django.shortcuts import render, redirect
from django.contrib.auth.decorators import login_required
from django.urls import reverse_lazy
from django.db.models import Q,F
from .models import *
from .viewsPlayer import *
from .viewsPublisher import *
from .utility import *
from django.contrib.auth.models import User
from .choices import *
from django.contrib.auth.decorators import user_passes_test




# Create your views here.

#controlli sui gruupi
#@user_passes_test(is_group_publisher_member)
#@user_passes_test(is_group_player_member)
#metti questo codice sopra la funzione da proteggere

def is_group_publisher_member(user):
    return user.groups.filter(name='Publisher').exists()

def is_group_player_member(user):
    return user.groups.filter(name='Player').exists()

def view_page2(request):
    
    #guarda se esiste una entry per lo user come player
    #se esiste controlla se la entry è gia popolata
    if request.user.groups.filter(name='Player').exists():
        try:
            player = Player.objects.get(user=request.user)
            if player.name:
                return player_home(request)
        except Player.DoesNotExist:
            pass
        return player_registration(request)
        
    
    
    if request.user.groups.filter(name='Publisher').exists():
        try:
            publisher = Publisher.objects.get(user=request.user)
            if publisher.name:
                return publisher_home(request)
        except Publisher.DoesNotExist:
            pass
        return publisher_registration(request)

    # Se l'utente non è né un player né un publisher, devono registrarsi.
    return render(request, template_name="ok.html")
    

def view_page(request):
    
    #se utente è un player fai il render di questa pagina per salvare le info nome cognome eccetera
    if request.user.groups.filter(name='Player').exists():
        player=Player.objects.get(user=request.user)
        return render(request, template_name="home_player.html", context= {'username': request.user.username,'player':player})
    if request.user.groups.filter(name='Publisher').exists():
        return render(request, template_name="publisherReg.html", context= {'username': request.user.username})
    #else è azienda

    return render(request, template_name="registrazione.html")


#-----------------publisher registration----------------------#

#-------------------------------------------#


#-------------------------------------------#
@login_required
@user_passes_test(is_group_publisher_member)
def game_registration(request):
    if request.method == 'POST':
        titolo = request.POST.get('titolo')
        price = request.POST.get('price')
        pict = request.FILES['pict']
        category=request.POST.get('category')
        age=request.POST.get('age')
        console=request.POST.get('console')
        description=request.POST.get('description')
        
    
        publisher=Publisher.objects.get(user=request.user)
        game = Game(titolo=titolo, publisher=publisher, price=price, category=category, pict=pict, age=age, console=console, description=description)
        game.save()
        
        images = request.FILES.getlist('images')

        # Controlla se sono state caricate meno di 10 immagini
        if len(images) > 10:
            return HttpResponse("Puoi caricare al massimo 10 immagini.")

        # Salva le immagini e associale al gioco
        for image in images:
            new_image = Image(image=image)
            new_image.save()
            game.images.add(new_image)
        registrazione_avvenuta = True  # Indica che la registrazione è andata a buon fine
        return render(request, 'gameRegistration.html', {'category_choices':CATEGORY_CHOICES, 'console_choices':CONSOLE_CHOICES,'registrazione_avvenuta': registrazione_avvenuta})

        
        
        return redirect('/gestione/publisherHome') 
    
    return render(request, 'gameRegistration.html',{'category_choices':CATEGORY_CHOICES, 'console_choices':CONSOLE_CHOICES})


def all_game(request):
      games = Game.objects.all().order_by('price')
      return render(request, 'gamePub.html', {'games': games})

#all
def view_add_game(request):
    if request.method == 'POST':
      
        game_id = request.POST.get('game_id')
        game = Game.objects.get(pk=game_id)
        if game in request.user.player.games.all():
            request.user.player.games.remove(game)
        else:
            request.user.player.games.add(game)
        
        return redirect('/gestione/view_game_details/'+game_id)

    #games = Game.objects.exclude(player=request.user.player).order_by('titolo')
    games=Game.objects.all
    
    publisher=Publisher.objects.all()
    return render(request, 'addgamePub.html', {'games': games,'p':publisher})


#game page: player can see add review... user and publisher no
def view_game_details(request, game_id):
    game = Game.objects.get(pk=game_id)
    images = game.images.all()
    reviews=Review.objects.filter(game=game)
    
    p=Player.objects.filter(games=game)
    n=len(p)
    
    if is_group_publisher_member(request.user):
        if request.method == "POST" and "sort_by" in request.POST:
            sort_by = request.POST["sort_by"]
            if sort_by == "asc":
                reviews = sorted(reviews, key=lambda x: (x.plot_rating + x.music_rating + x.gameplay_rating + x.performance_rating) / 4)
            elif sort_by == "des":
                reviews = sorted(reviews, key=lambda x: (x.plot_rating + x.music_rating + x.gameplay_rating + x.performance_rating) / 4, reverse=True)
            return render(request, "gamePage.html",{'game': game,'images':images ,'reviews':reviews,'n':n})

        return render(request, "gamePage.html", {'game': game, 'images':images,'reviews':reviews,'n':n})
        
    
    player=Player.objects.get(user=request.user)
    
    reviewed=0
    if reviews.filter(player=player, game=game):
        reviewed=Review.objects.get(player=player,game=game)
    
    player_games=set(player.games.all())
    
    #if hasattr(request, 'is_testing'):
    rec_game = get_recommended_games_by_added2(game, player, player_games)
    #else:
    #rec_game = None
    
    if request.method == "POST" and "sort_by" in request.POST:
        sort_by = request.POST["sort_by"]
        if sort_by == "asc":
            reviews = sorted(reviews, key=lambda x: (x.plot_rating + x.music_rating + x.gameplay_rating + x.performance_rating) / 4)
        elif sort_by == "des":
            reviews = sorted(reviews, key=lambda x: (x.plot_rating + x.music_rating + x.gameplay_rating + x.performance_rating) / 4, reverse=True)
        return render(request, "gamePage.html", {'game': game,'images':images, 'reviews':reviews,'player':player,'n':n,'rec_game':rec_game, 'reviewed':reviewed})

    
    return render(request, "gamePage.html", {'game': game,'images':images, 'reviews':reviews,'player':player,'n':n,'rec_game':rec_game, 'reviewed':reviewed})
    
    #games = Game.objects.get()
    #return render(request, "gamePage.html",{'games': games} )

def add_remove_game(request):
    if request.method == 'POST':
        game_id = request.POST.get('game_id')
        player = request.user.player  # Assuming you have a one-to-one relationship between User and Player
        game = Game.objects.get(id=game_id)

        if game in player.games.all():
            player.games.remove(game)
        else:
            player.games.add(game)

    return redirect('/gestione/addGames/')

@login_required
@user_passes_test(is_group_player_member)
def review_game(request, game_id):
    game = Game.objects.get(pk=game_id)
    player=Player.objects.get(user=request.user)
    if request.method == 'POST':
        if game not in player.games.all():
            error_message = "Non puoi recensire un gioco che non è nella tua lista."
            return render(request, 'ok.html', {'game': game, 'error_message': error_message})
        
        player=Player.objects.get(user=request.user)
        plot_rating = request.POST.get('plot_rating')
        gameplay_rating = request.POST.get('gameplay_rating')
        performance_rating = request.POST.get('performance_rating')
        music_rating = request.POST.get('music_rating')
        comment = request.POST.get('notes')
        
        try:
            review = Review.objects.create(game=game, player=player, plot_rating=plot_rating, performance_rating=performance_rating, music_rating=music_rating, gameplay_rating=gameplay_rating, comment=comment)
            review.save()
            registrazione_avvenuta = True  # Indica che la registrazione è andata a buon fine
            return render(request, 'reviewGame.html', {'game':game ,'registrazione_avvenuta': registrazione_avvenuta})
            #return redirect('/gestione/addGames')
        except IntegrityError:
            error_message = "Hai già recensito questo gioco."
            return render(request, 'reviewGame.html', {'game': game, 'error_message': error_message})
    return render(request, 'reviewGame.html', {'game': game})

@login_required
@user_passes_test(is_group_player_member)
def delete_review(request, review_id):
    review=Review.objects.get(id=review_id)
    game=review.game
    if request.method == 'POST':
        review.delete()
        return redirect('/gestione/view_game_details/'+str(game.id))
    return render(request, 'deleteReview.html', {'review': review})

@login_required
@user_passes_test(is_group_player_member)
def modify_review(request, review_id):
    review=Review.objects.get(id=review_id)
    player = Player.objects.get(user=request.user)
    game=review.game
    
    if request.method == 'POST':
        
        
        plot_rating = request.POST.get('plot_rating')
        gameplay_rating = request.POST.get('gameplay_rating')
        performance_rating = request.POST.get('performance_rating')
        music_rating = request.POST.get('music_rating')
        comment = request.POST.get('notes')

        # Elimina la vecchia recensione
        review.delete()
        

        # Crea una nuova recensione con i nuovi valori
        review = Review.objects.create(game=game, player=player, plot_rating=plot_rating, performance_rating=performance_rating, music_rating=music_rating, gameplay_rating=gameplay_rating, comment=comment)
        review.save()
        return redirect('/gestione/view_game_details/'+str(game.id))

    return render(request, 'reviewGame.html', {'game': game, 'review': review})
    
    


def filter_game_by_price(request):
    if request.method=='POST':
        min = request.POST.get('min_price')
        max = request.POST.get('max_price')
        console = request.POST.get('console-filter')
        category=request.POST.get('category-filter')
        pub=request.POST.get('pub-filter')
        if min:
            min = float(min)
        else:
            min = 0

        if max:
            max = float(max)
        else:
            max = 1000

        
    
    games = Game.objects.all()
    filtered_games = list(games)  


    if min >= 0 and max < 1000:
        filtered_games = [g for g in filtered_games if min <= g.price <= max]

    if console and console!="all":
        filtered_games = [g for g in filtered_games if g.console == console]

    if category and category!="all":
        filtered_games = [g for g in filtered_games if g.category == category]
    if pub and pub!="all":
        filtered_games = [g for g in filtered_games if g.publisher.name == pub]

    request.session['filtered_games'] = [game.id for game in filtered_games]
    p=Publisher.objects.all() 
    return render(request, 'addgamePub.html', {'games': filtered_games, 'p':p})

def filter_game_by_rating(request):
    filtered_games = request.session.get('filtered_games', [])
    if not filtered_games:
        filtered_games=Game.objects.all()
    
    sort_by=request.POST.get('sort_by')
    if sort_by == 'rating':
        games = Game.objects.filter(id__in=filtered_games).annotate(
            media=(F('average_plot_rating') + F('average_music_rating') + 
                   F('average_gameplay_rating') + F('average_performance_rating')) / 4
        ).order_by('-media')
    elif sort_by == 'priceA':
        games = Game.objects.filter(id__in=filtered_games).order_by('price')
    elif sort_by == 'priceD':
        games = Game.objects.filter(id__in=filtered_games).order_by('-price')
    elif sort_by == 'added':
        sorted_games = sort_games_by_most_added(filtered_games)
        games=sorted_games
    p=Publisher.objects.all() 
    return render(request, 'addgamePub.html', {'games': games, 'p':p})
        
def filter_game_by_name(request):
    games=Game.objects.all()
    if request.method=='POST':
        title=request.POST.get('game_name')
        games = Game.objects.filter(Q(titolo=title) | Q(titolo__startswith=title))
        request.session['filtered_games'] = [game.id for game in games]  
        p=Publisher.objects.all() 
        return render(request, 'addgamePub.html', {'games': games,'p':p})
    
    
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

@login_required
@user_passes_test(is_group_player_member) 
def new_test(request):
    #devo passare
    #top rated games (3) most added ok
    #suggested games ....
    #since you added ... you may also consider to add ....
    games=Game.objects.all()
    player=Player.objects.get(user=request.user)

    top_games=get_most_added_games(games)
    playerGames=set(player.games.all())
    
    recgames=[]
    for singleGame in playerGames:
        recommended=get_recommended_games_by_added(singleGame,player,playerGames) 
        if recommended:
            recgames.append([singleGame] + recommended)
    
    category_game= get_recommended_games_by_category_added(playerGames)
    
    
    
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
    
    return render(request,'searchgames.html',{'games':games, 'top_games':top_games, 'recgames':recgames, 'category_game':category_game, 'sug_games':suggested_games})



def todel(request):
    games=Game.objects.all()
    return render(request,"newtzt.html",{'games':games})


def search_player(request):
    
    if request.user.is_anonymous:
        players_game={}
        for p in Player.objects.all():
            players_game[p]=0
            
        if request.method == 'POST':
            sort_by = request.POST.get('sort_by')
            if sort_by == 'name':
                players_game_sorted = dict(sorted(players_game.items(), key=lambda item: item[0].user.username))
            if sort_by == 'similar':
                players_game_sorted = dict(sorted(players_game.items(), key=lambda item: item[1], reverse=True))
            return render(request, 'playersPage.html', {'players': players_game_sorted})
        return render(request, 'playersPage.html', {'players': players_game})
    
    if request.user.groups.filter(name='Publisher').exists():
        is_pub=1
        publisher=Publisher.objects.get(user=request.user)
        players=Player.objects.all()
        games=Game.objects.filter(publisher=publisher)
        players_game={}
        for p in players:
            players_game[p]= len(Game.objects.filter(publisher=publisher, id__in=p.games.all()))
        if request.method == 'POST':
            sort_by = request.POST.get('sort_by')
            if sort_by == 'name':
                players_game_sorted = dict(sorted(players_game.items(), key=lambda item: item[0].user.username))
            if sort_by == 'similar':
                players_game_sorted = dict(sorted(players_game.items(), key=lambda item: item[1], reverse=True))
            return render(request, 'playersPage.html', {'players': players_game_sorted,'is_pub':is_pub})
        return render(request, 'playersPage.html', {'players': players_game, 'is_pub':is_pub})  
        
    
    players=Player.objects.exclude(user=request.user)
    p1=Player.objects.get(user=request.user)
    p1_games=set(p1.games.all())
    players_game={}
    
    for p in players:
        gamep = set(p.games.all())
        common_games = p1_games.intersection(gamep)
        players_game[p] = len(common_games)
        
    if request.method == 'POST':
        sort_by = request.POST.get('sort_by')
        if sort_by == 'name':
            players_game_sorted = dict(sorted(players_game.items(), key=lambda item: item[0].user.username))
        if sort_by == 'similar':
            players_game_sorted = dict(sorted(players_game.items(), key=lambda item: item[1], reverse=True))

        return render(request, 'playersPage.html', {'players': players_game_sorted,'p1':p1})

        
    
    return render(request, 'playersPage.html', {'players': players_game,'p1':p1})


def search_publisher(request):
    publishers=Publisher.objects.all()
    
    if request.user.is_anonymous or request.user.groups.filter(name='Publisher').exists():
        is_an=1
        publisher_game={}
        for publisher in publishers:
            publisher_game[publisher]=0
        if request.method == 'POST':
            sort_by = request.POST.get('sort_by')
            if sort_by == 'name':
                publisher_game_sorted = dict(sorted(publisher_game.items(), key=lambda item: item[0].name))
            if sort_by == 'similar':
                publisher_game_sorted = dict(sorted(publisher_game.items(), key=lambda item: item[1], reverse=True))

            return render(request, 'publishersPage.html', {'publisher_game':publisher_game_sorted,'is_an':is_an})
        return render(request, 'publishersPage.html', {'publisher_game':publisher_game,'is_an':is_an})
    
  
    
            
        
        
    p1=Player.objects.get(user=request.user)
    
    games=Game.objects.all()
    
    usergames=set(p1.games.all())
    publisher_game={}
    
    for publisher in publishers:
        game=Game.objects.filter(publisher=publisher)
        count=0
        for g in game:
            for g1 in usergames:
                if g==g1:
                    count +=1
        publisher_game[publisher]=count
        
    if request.method == 'POST':
        sort_by = request.POST.get('sort_by')
        if sort_by == 'name':
            publisher_game_sorted = dict(sorted(publisher_game.items(), key=lambda item: item[0].name))
        if sort_by == 'similar':
            publisher_game_sorted = dict(sorted(publisher_game.items(), key=lambda item: item[1], reverse=True))

        return render(request, 'publishersPage.html', {'publisher_game':publisher_game_sorted, 'p1':p1})
    
    return render(request, 'publishersPage.html', {'publisher_game':publisher_game, 'p1':p1})


@login_required
@user_passes_test(is_group_publisher_member)
def analytics_game(request, game_id):
    
    game=Game.objects.get(pk=game_id)
    publisher = Publisher.objects.get(user=request.user)
    
    if game.publisher != publisher:
        return redirect('/gestione/publisherHome')
    
    if request.method == 'POST':
        min_age = request.POST.get('min_age')
        max_age = request.POST.get('max_age')

        if min_age and max_age:
            player = Player.objects.filter(games=game, age__gte=min_age, age__lte=max_age)
            reviews = Review.objects.filter(player__in=player, game=game)
        else:
            reviews = Review.objects.filter(game=game)
    else:
        player=Player.objects.filter(games=game)
        reviews = Review.objects.filter(game=game)
    
    
    averageAge= calc_average(player)
    
    n=0
    
   
    for r in reviews:
        n+=1
    
    if n > 0:
        statList = average_review_stat(reviews, n)
        
    else:
        statList ={
            'plot' : 0,
            'gameplay' :0,
            'music' : 0,
            'performance' : 0
        }
    
   
    
    av = round(average_rev(reviews, len(reviews)), 2)
    location_dict=get_location(player)
    
    countryL = list(location_dict.keys())
    occurrency = list(location_dict.values())
    
    country_codes = [country.code for country in countryL]

    return render(request, 'analyticsGame.html', {'occurrency':occurrency,'country':country_codes, 'av':av,
                                                  'game':game,'player':player, 'average_age':averageAge, 'n':n,'review':statList,'reviews':reviews})
        

