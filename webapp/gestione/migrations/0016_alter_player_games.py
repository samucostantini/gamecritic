# Generated by Django 4.2.5 on 2023-10-02 10:18

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('gestione', '0015_remove_player_game_player_games'),
    ]

    operations = [
        migrations.AlterField(
            model_name='player',
            name='games',
            field=models.ManyToManyField(to='gestione.game'),
        ),
    ]
