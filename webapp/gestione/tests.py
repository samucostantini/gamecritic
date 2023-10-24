from django.test import TestCase, Client
from django.contrib.auth.models import User
# Create your tests here.
from .models import Player
from .models import Game
from .models import Publisher
from .utility import calc_average, get_recommended_games_by_added2
from .utility import get_recommended_games_by_category_added
from .views import *
from django.urls import reverse

class Persona:
    def __init__(self, name, age):
        self.name = name
        self.age = age

class PlayerTestCase(TestCase):
    
    def test_calc_average(self):
        # Creazione di giocatori di prova
        persona1 = Persona(name="1", age=25)
        persona2 = Persona(name="2", age=30)
        persona3 = Persona(name="3", age=20)
        
        players = [persona1, persona2, persona3]
        # Verifica se la media viene calcolata correttamente
        self.assertAlmostEqual(calc_average(players), 25.0, places=5,msg="age test + player OK")
        
        
        players=[persona1]
        self.assertAlmostEqual(calc_average(players), 25.0, places=5,msg="age test 1 player ok")
        
        players=[]
        self.assertAlmostEqual(calc_average(players), 0.0, places=5,msg="age test 0 player OK")
        
        
class RecommendationTestCase(TestCase):
    
    def setUp(self):
        user = User.objects.create_user(username='example_user', password='example_password')
        user2 = User.objects.create_user(username='example_userp', password='example_password')
        user3 = User.objects.create_user(username='example_userp2', password='example_password')
        user4 = User.objects.create_user(username='example_usferp2', password='example_password')
        
        publisher= Publisher.objects.create(
            user=user,
            name="Example Publisher",
            website="http://www.example.com",
            pict="publisher_img/example.jpg"
        )
        # Crea alcuni giochi
        self.game1 = Game.objects.create(
            titolo="Game 1",
            publisher=publisher,
            price=50,
            category="Action",
            age=18,
            pict="static/game_img/game1.jpg",
            description="Description for Game 1",
            console="PS4",
            average_plot_rating=4.5,
            average_music_rating=3.8,
            average_gameplay_rating=4.2,
            average_performance_rating=4.0,
            total_reviews=100
        )
        self.game2 = Game.objects.create(
            titolo="Game 2",
            publisher=publisher,
            price=50,
            category="Action",
            age=18,
            pict="static/game_img/game1.jpg",
            description="Description for Game 1",
            console="PS4",
            average_plot_rating=4.5,
            average_music_rating=3.8,
            average_gameplay_rating=4.2,
            average_performance_rating=4.0,
            total_reviews=100
        )
        
        self.game3 = Game.objects.create(
            titolo="Game 3",
            publisher=publisher,
            price=40,
            category="Adventure",
            age=16,
            pict="static/game_img/game2.jpg",
            description="Description for Game 2",
            console="Xbox One",
            average_plot_rating=4.0,
            average_music_rating=4.2,
            average_gameplay_rating=4.5,
            average_performance_rating=4.3,
            total_reviews=120
        )
        
        self.game4 = Game.objects.create(
            titolo="Game 4",
            publisher=publisher,
            price=60,
            category="Action",
            age=20,
            pict="static/game_img/game3.jpg",
            description="Description for Game 3",
            console="PS5",
            average_plot_rating=4.2,
            average_music_rating=3.9,
            average_gameplay_rating=4.3,
            average_performance_rating=4.1,
            total_reviews=80
        )
        
        self.game5 = Game.objects.create(
            titolo="Game 5",
            publisher=publisher,
            price=60,
            category="Action",
            age=20,
            pict="static/game_img/game3.jpg",
            description="Description for Game 3",
            console="PS5",
            average_plot_rating=4.2,
            average_music_rating=3.9,
            average_gameplay_rating=4.3,
            average_performance_rating=4.1,
            total_reviews=82
        )
        
        # Crea un giocatore e associa loro alcuni giochi
        self.player1 = Player.objects.create(
            user=user2,
            name="Alice",
            surname="Alice",
            age=21,
            pict="static/player_img/alice.jpg",
            console="PS4",
            country="US"
        )
        
        self.player2 = Player.objects.create(
            user=user3,
            name="Bob",
            surname="Bob",
            age=21,
            pict="static/player_img/alice.jpg",
            console="PS4",
            country="US"
        )
        self.player3 = Player.objects.create(
            user=user4,
            name="Bob",
            surname="Bob",
            age=21,
            pict="static/player_img/alice.jpg",
            console="PS4",
            country="US"
        )
        
       
    
    def test_get_recommended_games_by_category_added(self):
        self.player1.games.set([])
        self.player2.games.set([self.game4,self.game5])
        self.player3.games.set([self.game5])
       
        #caso persona con giochi (azione azione avventura)-> preferita=azione cerca tra i giochi azione (game4,game5) quello piu aggiunto game 5
        player_games = [self.game1, self.game2, self.game3]
        recommended_game = get_recommended_games_by_category_added(player_games)
        self.assertEqual(recommended_game, self.game5)

        #caso persona con giochi (avventura)-> preferita=avventura cerca tra i giochi di categoria avventura(non presenti)
        player_games = [self.game3]
        recommended_game = get_recommended_games_by_category_added(player_games)
        self.assertEqual(recommended_game, 0)
        
        #caso persona con giochi (all)-> preferita=azione cerca tra i giochi non aggiunti cioè nessuno
        player_games = [self.game1,self.game2,self.game3,self.game4,self.game5]
        recommended_game = get_recommended_games_by_category_added(player_games)
        self.assertEqual(recommended_game, 0)
        
        #caso persona non ha giochi aggiunti, viene ritornato il gioco piu aggiunto
        player_games = []
        recommended_game = get_recommended_games_by_category_added(player_games)
        self.assertEqual(recommended_game, self.game5)
        
        
        self.player3.games.set([])
        player_games = [self.game1, self.game2, self.game3]
        recommended_game = get_recommended_games_by_category_added(player_games)
        self.assertEqual(recommended_game, self.game4)

        self.player2.games.set([])
        self.player3.games.set([])
        player_games = [self.game1, self.game2, self.game3]
        recommended_game = get_recommended_games_by_category_added(player_games)
        self.assertEqual(recommended_game, 0)
        
        self.player2.games.set([self.game2,self.game3,self.game4])
        self.player3.games.set([self.game2])
        player_games = [self.game1, self.game2, self.game3]
        recommended_game = get_recommended_games_by_category_added(player_games)
        self.assertEqual(recommended_game, self.game4)
        

class RecommendationTestCaseAdded(TestCase):
    
    def setUp(self):
        user = User.objects.create_user(username='example_user', password='example_password')
        user2 = User.objects.create_user(username='example_userp', password='example_password')
        user3 = User.objects.create_user(username='example_userp2', password='example_password')
        user4 = User.objects.create_user(username='example_usersp2', password='example_password')
        
        publisher= Publisher.objects.create(
            user=user,
            name="Example Publisher",
            website="http://www.example.com",
            pict="publisher_img/example.jpg"
        )
        # Crea alcuni giochi
        self.game1 = Game.objects.create(
            titolo="Game 1",
            publisher=publisher,
            price=50,
            category="Action",
            age=18,
            pict="static/game_img/game1.jpg",
            description="Description for Game 1",
            console="PS4",
            average_plot_rating=4.5,
            average_music_rating=3.8,
            average_gameplay_rating=4.2,
            average_performance_rating=4.0,
            total_reviews=100
        )
        self.game2 = Game.objects.create(
            titolo="Game 2",
            publisher=publisher,
            price=50,
            category="Adventure",
            age=18,
            pict="static/game_img/game1.jpg",
            description="Description for Game 1",
            console="PS4",
            average_plot_rating=4.5,
            average_music_rating=3.8,
            average_gameplay_rating=4.2,
            average_performance_rating=4.0,
            total_reviews=100
        )
        
        self.game3 = Game.objects.create(
            titolo="Game 3",
            publisher=publisher,
            price=40,
            category="Adventure",
            age=16,
            pict="static/game_img/game2.jpg",
            description="Description for Game 2",
            console="Xbox One",
            average_plot_rating=4.0,
            average_music_rating=4.2,
            average_gameplay_rating=4.5,
            average_performance_rating=4.3,
            total_reviews=120
        )
        
        self.game4 = Game.objects.create(
            titolo="Game 4",
            publisher=publisher,
            price=60,
            category="Action",
            age=20,
            pict="static/game_img/game3.jpg",
            description="Description for Game 3",
            console="PS5",
            average_plot_rating=4.2,
            average_music_rating=3.9,
            average_gameplay_rating=4.3,
            average_performance_rating=4.1,
            total_reviews=80
        )
        
        self.game5 = Game.objects.create(
            titolo="Game 5",
            publisher=publisher,
            price=60,
            category="Action",
            age=20,
            pict="static/game_img/game3.jpg",
            description="Description for Game 3",
            console="PS5",
            average_plot_rating=4.2,
            average_music_rating=3.9,
            average_gameplay_rating=4.3,
            average_performance_rating=4.1,
            total_reviews=82
        )
        
        # Crea un giocatore e associa loro alcuni giochi
        self.player1 = Player.objects.create(
            user=user2,
            name="Alice",
            surname="Alice",
            age=21,
            pict="static/player_img/alice.jpg",
            console="PS4",
            country="US"
        )
        
        self.player2 = Player.objects.create(
            user=user3,
            name="Bob",
            surname="Bob",
            age=21,
            pict="static/player_img/alice.jpg",
            console="PS4",
            country="US"
        )
        self.player3 = Player.objects.create(
            user=user4,
            name="Bob",
            surname="Bob",
            age=21,
            pict="static/player_img/alice.jpg",
            console="PS4",
            country="US"
        )
        
        self.player2.games.set([self.game1,self.game2])
        self.player3.games.set([self.game1,self.game2,self.game3])
       
        
    def test_get_recommended_games_by_added2(self):
        # Case: Giocatore 1 cerca raccomandazioni per gioco 1 (senza averlo aggiunto)
        
        self.player2.games.set([self.game1,self.game2])
        self.player3.games.set([self.game1,self.game2,self.game3])
        
        player_game = self.game1
        player = self.player1
        player_games = set([])
        suggested_game = get_recommended_games_by_added2(player_game, player, player_games)
        self.assertEqual(suggested_game, self.game2) #ok
        
        # Case: Giocatore 1 cerca raccomandazioni per gioco 1 (aggiunto)
        player_game = self.game1
        player = self.player1
        player_games = set([self.game1])
        suggested_game = get_recommended_games_by_added2(player_game, player, player_games)
        self.assertEqual(suggested_game, self.game2) #ok

       # Case: Giocatore 1 ha aggiunto il gioco1 2 e 3 e cerca raccomandazioni per gioco 1, risultato nullo, sarebbe 2 ma è nella sua lista
        player_game = self.game1
        player = self.player2
        player_games = set([self.game1, self.game2, self.game3])
        suggested_game = get_recommended_games_by_added2(player_game, player, player_games)
        self.assertIsNone(suggested_game)

        # Scenario: Giocatore 1 ha aggiunto il gioco 1 e cerca raccomandazioni per 2
        
        player_game = self.game2
        player = self.player1
        player_games = set([self.game1])
        suggested_game = get_recommended_games_by_added2(player_game, player, player_games)
        self.assertEqual(suggested_game,self.game3)

        self.player2.games.set([])
        self.player3.games.set([])
        player_game = self.game2
        player = self.player1
        player_games = set([self.game1])
        suggested_game = get_recommended_games_by_added2(player_game, player, player_games)
        self.assertIsNone(suggested_game,None)



class TestGameDetailsView(TestCase):
    def setUp(self):
        # Crea un utente
        self.user = User.objects.create_user(username='example_user', password='example_password')

        # Crea un publisher
        self.publisher = Publisher.objects.create(
            user=self.user,
            name="Example Publisher",
            website="http://www.example.com",
            pict="publisher_img/example.jpg"
        )

        # Crea un giocatore
        self.player = Player.objects.create(
            user=self.user,
            name="Alice",
            surname="Alice",
            age=21,
            pict="static/player_img/alice.jpg",
            console="PS4",
            country="US"
        )

        # Crea un gioco
        self.game = Game.objects.create(
            id=1,
            titolo="Game 1",
            publisher=self.publisher,
            price=50,
            category="Action",
            age=18,
            pict="static/game_img/game1.jpg",
            description="Description for Game 1",
            console="PS4",
            average_plot_rating=4.5,
            average_music_rating=3.8,
            average_gameplay_rating=4.2,
            average_performance_rating=4.0,
            total_reviews=100
        )

        # Crea una recensione
        self.review = Review.objects.create(
            game=self.game,
            player=self.player,
            plot_rating=4,
            music_rating=3,
            gameplay_rating=5,
            performance_rating=4,
            comment="Great game!"
        )

    def test_view_game_details(self):
        self.client.login(username="example_user", password="example_password")

        url = f'/gestione/view_game_details/{self.game.id}/'

        response = self.client.get(url)

        self.assertEqual(response.status_code, 200)
        self.assertContains(response, 'game')
        self.assertContains(response, 'reviews')
        self.assertContains(response, 'player')
        self.assertContains(response, 'n')
       
        