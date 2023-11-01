from django.urls import include,path
from django.contrib import admin
from .forms import *
from .views import *
from .viewsPlayer import *
from .viewsPublisher import *

app_name='gestione'

urlpatterns = [
    
    path('admin/', admin.site.urls),
    path('', view_page2, name='viewPage'),
    path('home/', view_page2, name='viewPage'),
    path('playerHome/', player_home, name='player_home'),
    path('playerReg/', player_registration, name='player_registration'),
    path('playerProfile/<int:player_id>/',player_profile, name='player_profile'),
    #path('playerProfile/<int:player_id>/',player_profile, name='player_profile'),
    path('publisherHome/', publisher_home, name='publisher_home'),
    path('publisherReg/', publisher_registration, name='publisher_registration'),
    path('publisherEdit/', edit_publisher_profile, name=' edit_publisher_profile'),
    path('playerEdit/', edit_player_profile, name=' edit_player_profile'),
    path('publisherProfile/<int:publisher_id>/', publisher_profile, name='publisher_profile'),
    #path('publisherProfile/<int:publisher_id>/', publisher_profile, name='publisher_profile'),
    path('gameReg/', game_registration, name='game_registration'),
    path('gamePub/', show_publisher_game, name='show_publisher_game'),
    
    #path('home2/',all_game,name="home2"),
    path('allGame/',all_game,name="all_game"),
    
    #page per aggiungere giochi e recensioni
    path('addGames/', view_add_game,name='view_add_game'),
    path('view_game_details/<int:game_id>/', view_game_details,name='view_game_details'),
    path('reviewGame/<int:game_id>/', review_game,name='review_game'),
    
    path('filterGames/', filter_game_by_price, name='filter_game_by_price'),
    path('filterGamesbyRate/', filter_game_by_rating, name='filter_game_by_price'),
    path('filterGamebyName/', filter_game_by_name, name="filter_game_by_name"),
    #pagina per publisher per vedere recensioni di giochi
    path('gameStat/<int:game_id>/',show_game_stat,name='show_game_stat'),
    path('gameAnalytics/<int:game_id>/',analytics_game,name='analytics_game'),

    path('gameRecm/',new_test,name="game_recommended"),
    path('myGames/',my_games,name="my_games"),
    
    path('modifyReview/<int:review_id>/',modify_review,name='modify_review'),
    path('deleteReview/<int:review_id>/',delete_review,name='delete_review'),
    
    path('specSearch/',specSearch,name='specSearch'),
    path('test/',new_test,name="new_test"),
    path('todel/',todel,name="nn"),
    path('analyzeAll/',show_allGames_stat,name='show_allGames_stat'),
    
    path('playersPage/',search_player,name='search_player'),
    path('publishersPage/',search_publisher,name='search_publisher'),
    
    path('addRemoveGame/',add_remove_game,name='add_remove_game'),

]
