# Generated by Django 4.2.5 on 2023-10-02 09:51

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('gestione', '0011_alter_player_game'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='player',
            name='game',
        ),
        migrations.AddField(
            model_name='player',
            name='game',
            field=models.ForeignKey(default=0, on_delete=django.db.models.deletion.CASCADE, to='gestione.game'),
        ),
    ]
