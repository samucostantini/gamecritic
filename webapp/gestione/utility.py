from django.db import IntegrityError
from django.shortcuts import render, redirect
from django.contrib.auth.decorators import login_required
from django.urls import reverse_lazy

from .models import Player
from .models import Game
from .models import Review
from .models import Publisher
from .viewsPublisher import *
from django.contrib.auth.models import User


def calc_average(players):
    total_age = 0
    num_players = 0
    
    for player in players:
        total_age += player.age
        num_players += 1
    
    if num_players > 0:
        average_age = total_age / num_players
        return average_age
    else:
        return 0
    
def average_rev(review,n):
    plot_rating=0
    music_rating=0
    performance_rating=0
    gameplay_rating=0
    
    
    for r in review:
        plot_rating += r.plot_rating
        music_rating += r.music_rating
        performance_rating += r.performance_rating
        gameplay_rating += r.gameplay_rating
        
    plot_rating=plot_rating/n
    music_rating=music_rating/n
    performance_rating=performance_rating/n
    gameplay_rating=gameplay_rating/n 
    
    
    
    return (plot_rating+music_rating+performance_rating+gameplay_rating)/4
    

def average_review_stat(review, n) :
    
    plot_rating=0
    music_rating=0
    performance_rating=0
    gameplay_rating=0
    
    
    for r in review:
        plot_rating += r.plot_rating
        music_rating += r.music_rating
        performance_rating += r.performance_rating
        gameplay_rating += r.gameplay_rating
        
    plot_rating=plot_rating/n
    music_rating=music_rating/n
    performance_rating=performance_rating/n
    gameplay_rating=gameplay_rating/n
    
    return {
        'plot' : plot_rating,
        'gameplay' : gameplay_rating,
        'music' : music_rating,
        'performance' : performance_rating
    }

def get_location(player):
    
    location_count={}
    for p in player:
        if p.country not in location_count:
            location_count[p.country] = 1  # If the location is not in the dictionary, add it with a count of 1
        else:
            location_count[p.country] += 1  # If the location is already in the dictionary, increment the count
    
    return location_count



def get_recommended_games_by_added(player_game,player,playerGames):
    other_player=Player.objects.exclude(id=player.id)
    
    
    suggested_games_weights = {}

    for p in other_player:
        other_games = set(p.games.all())
        
        if player_game in other_games:
            for gam in other_games:
                if gam != player_game:
                    suggested_games_weights[gam] = suggested_games_weights.get(gam, 0) + 1
                    
    suggested_games = sorted(suggested_games_weights.items(), key=lambda x: x[1], reverse=True)[:2]     
    
    filtered_suggested_games = []
    
    for game, _ in suggested_games:
        if game not in playerGames:
            filtered_suggested_games.append((game, _))
    
    return filtered_suggested_games

def get_recommended_games_by_added2(player_game,player,playerGames):
    other_player=Player.objects.exclude(id=player.id)
    
    
    suggested_games_weights = {}

    for p in other_player:
        other_games = set(p.games.all())
        
        if player_game in other_games:
            for gam in other_games:
                if gam != player_game:
                    suggested_games_weights[gam] = suggested_games_weights.get(gam, 0) + 1
                    
    suggested_game = sorted(suggested_games_weights, key=lambda x: suggested_games_weights[x] , reverse=True)
    
    for game in suggested_game:
        if suggested_games_weights[game] >= 1 and game not in playerGames:
            return game
    return None

def sort_games_by_most_added(games):
    game_counts={}
    for g in games:
        players=Player.objects.filter(games=g)
        n=len(players)
        game_counts[g]=n
    sorted_games = sorted(game_counts.keys(), key=lambda x: game_counts[x], reverse=True)

    return sorted_games
    

def get_recommended_games_by_category_added(player_games):
    
    if not player_games:
        return get_most_added_games2(Game.objects.all())
    
    games=Game.objects.all()
    games_copy = list(games)
    
    for g in games:
        for g2 in player_games:
            if g==g2:
                games_copy.remove(g)
            
    category_count = {}

    for game in player_games:
        category = game.category
        if category in category_count:
            category_count[category] += 1
        else:
            category_count[category] = 1

    max_category = max(category_count, key=category_count.get)
    
    game_counts = {}

    for g in games_copy:
        if g.category == max_category:
            players = Player.objects.filter(games=g)
            num_players=0
            if players:
                num_players = len(players)
                game_counts[g] = game_counts.get(g, 0) + num_players
           
    if not game_counts:
        return 0
    
    rec_game = max(game_counts, key=game_counts.get)
    
    if rec_game:
        return rec_game
    else:
        return 0



def get_most_added_games(games):
    game_counts={}
    for g in games:
        players=Player.objects.filter(games=g)
        n=len(players)
        game_counts[g]=n
    sorted_games = sorted(game_counts.keys(), key=lambda x: game_counts[x], reverse=True)

    # Restituisci i primi tre giochi
    top_three_games = sorted_games[:3]
    return top_three_games

def get_most_added_games2(games):
    game_counts={}
    for g in games:
        players=Player.objects.filter(games=g)
        n=len(players)
        game_counts[g]=n
    sorted_games = sorted(game_counts.keys(), key=lambda x: game_counts[x], reverse=True)

    # Restituisci i primi tre giochi
    top_three_games = sorted_games[0]
    return top_three_games