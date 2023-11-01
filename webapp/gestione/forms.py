from django import forms
from .models import Player
from .models import Game


class PlayerForm(forms.ModelForm):
    class Meta:
        model = Player
        exclude = ['user', 'games']
    def __init__(self, *args, **kwargs):
        user = kwargs.pop('user', None)  # Ottieni l'utente dai kwargs
        super(PlayerForm, self).__init__(*args, **kwargs)
        if user:
            self.instance.user = user
            
            
class GameRegistrationForm(forms.ModelForm):
    class Meta:
        model = Game
        fields = ['titolo', 'price', 'pict', 'category', 'age', 'console', 'description']
        widgets = {
            'description': forms.Textarea(attrs={'rows': 5}),
            'publisher': forms.HiddenInput()
        }

   

   