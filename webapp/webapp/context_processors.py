from gestione.choices import CATEGORY_CHOICES  # Assumi che il tuo file sia situato in questa directory
from gestione.choices import CONSOLE_CHOICES  # Assumi che il tuo file sia situato in questa directory
from gestione.choices import CATEGORY_CHOICES2  # Assumi che il tuo file sia situato in questa directory
from gestione.choices import CONSOLE_CHOICES2  # Assumi che il tuo file sia situato in questa directory

#se aggiungi vai a modificare in settings.py dentro templates

def category_choices_processor(request):
    return {'category_choices': CATEGORY_CHOICES}
def console_choices_processor(request):
    return {'console_choices': CONSOLE_CHOICES}
def category_choices_processor2(request):
    return {'category_choices': CATEGORY_CHOICES2}
def console_choices_processor2(request):
    return {'console_choices': CONSOLE_CHOICES2}