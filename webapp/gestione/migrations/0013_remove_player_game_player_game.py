# Generated by Django 4.2.5 on 2023-10-02 09:52

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('gestione', '0012_remove_player_game_player_game'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='player',
            name='game',
        ),
        migrations.AddField(
            model_name='player',
            name='game',
            field=models.ManyToManyField(blank=True, to='gestione.game'),
        ),
    ]
