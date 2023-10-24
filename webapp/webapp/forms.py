from django import forms
from django.contrib.auth.forms import UserCreationForm
from django.contrib.auth.models import Group
from django.contrib.auth.models import User

class CreateUser(UserCreationForm):
    class Meta:
        model = User
        fields = ['username', 'email']
        
    def save(self,commit=True):
        user=super().save(commit)
        g=Group.objects.get(name="Gruppo")
        return user
    
#-------uso questi per associare utente registrato a uno dei due gruppi------#

class CreatePlayer(UserCreationForm):
     def save(self, commit=True):
        user = super().save(commit) #ottengo un riferimento all'utente
        g = Group.objects.get(name="Player") #cerco il gruppo che mi interessa
        g.user_set.add(user) #aggiungo l'utente al gruppo
        return user

class CreatePublisher(UserCreationForm):
    
    def save(self, commit=True):
        user = super().save(commit) 
        g = Group.objects.get(name="Publisher") 
        g.user_set.add(user) 
        return user

