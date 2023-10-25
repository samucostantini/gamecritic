from django import forms
from .models import Player

class PlayerForm(forms.ModelForm):
    class Meta:
        model = Player
        exclude = ['user', 'games']
    def __init__(self, *args, **kwargs):
        user = kwargs.pop('user', None)  # Ottieni l'utente dai kwargs
        super(PlayerForm, self).__init__(*args, **kwargs)
        if user:
            self.instance.user = user