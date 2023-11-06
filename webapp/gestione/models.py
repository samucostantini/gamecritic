from django.db import models
from django.core.validators import MinValueValidator, MaxValueValidator

from django.contrib.auth.models import User
from django_countries.fields import CountryField

from multiselectfield import MultiSelectField

from .choices import *
from django.db.models import Avg
# Create your models here.

#devo fare 3 models: Player, Publisher, Game

#relazione 1 a molti tra Publisher e Game




class Publisher(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE)
    name = models.CharField(max_length=100, unique=True)
    website=models.CharField(max_length=100)
    pict=models.ImageField(upload_to="static/publisher_img",blank=True, null=True,default="null")
    

class Image(models.Model):
    image = models.ImageField(upload_to="static/game_img", blank=True, null=True,default="null")


class Game(models.Model):
    
    
    titolo = models.CharField(max_length=100)
    publisher = models.ForeignKey(Publisher, on_delete=models.CASCADE)
    price = models.IntegerField()
    category=models.CharField(max_length=20, choices=CATEGORY_CHOICES)
    age=models.IntegerField()
    
    pict=models.ImageField(upload_to="static/game_img", blank=True, null=True,default="null")
    description=models.TextField()
    console = models.CharField(max_length=20, choices=CONSOLE_CHOICES)  #valuta se togliere

    average_plot_rating = models.FloatField(default=0)
    average_music_rating = models.FloatField(default=0)
    average_gameplay_rating = models.FloatField(default=0)
    average_performance_rating = models.FloatField(default=0)
    total_reviews = models.PositiveIntegerField(default=0)
    
    images = models.ManyToManyField(Image, blank=True)
    
    class Meta:
        unique_together = ('titolo', 'console')

    def update_average_ratings(self):
        reviews = Review.objects.filter(game=self)
        if reviews.exists():
            self.average_plot_rating = reviews.aggregate(Avg('plot_rating'))['plot_rating__avg']
            self.average_music_rating = reviews.aggregate(Avg('music_rating'))['music_rating__avg']
            self.average_gameplay_rating = reviews.aggregate(Avg('gameplay_rating'))['gameplay_rating__avg']
            self.average_performance_rating = reviews.aggregate(Avg('performance_rating'))['performance_rating__avg']
            self.total_reviews = reviews.count()
        else:
            self.average_plot_rating = 0
            self.average_music_rating = 0
            self.average_gameplay_rating = 0
            self.average_performance_rating = 0
            self.total_reviews = 0

        self.save()

class Player(models.Model):
    
    user = models.OneToOneField(User, on_delete=models.CASCADE)
    name=models.CharField(max_length=100)
    surname=models.CharField(max_length=100)
    age=models.PositiveIntegerField()
    pict=models.ImageField(upload_to="static/player_img", blank=True, null=True,default="null")
    console = models.CharField(max_length=255, choices=CONSOLE_CHOICES, blank=True, null=True)
    games=models.ManyToManyField(Game)
    country = CountryField()
    
    def get_consoles(self):
        if self.console:
            return ', '.join(self.console.split(','))
        return ""
    

class Review(models.Model):
    game = models.ForeignKey(Game, on_delete=models.CASCADE)
    player = models.ForeignKey(Player, on_delete=models.CASCADE)
    plot_rating = models.PositiveIntegerField(default=1, validators=[MinValueValidator(1), MaxValueValidator(5)])
    music_rating = models.PositiveIntegerField(default=1, validators=[MinValueValidator(1), MaxValueValidator(5)])
    gameplay_rating = models.PositiveIntegerField(default=1, validators=[MinValueValidator(1), MaxValueValidator(5)])
    performance_rating = models.PositiveIntegerField(default=1, validators=[MinValueValidator(1), MaxValueValidator(5)])
    comment = models.TextField()
    class Meta:
        unique_together = ('game', 'player',)
    def save(self, *args, **kwargs):
        super(Review, self).save(*args, **kwargs)
        self.game.update_average_ratings()
    def delete(self, *args, **kwargs):
        super(Review, self).delete(*args, **kwargs)
        self.game.update_average_ratings()
        
        
