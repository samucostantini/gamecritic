# Generated by Django 4.2.5 on 2023-10-22 14:03

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('gestione', '0024_alter_game_console_alter_player_console'),
    ]

    operations = [
        migrations.AlterField(
            model_name='publisher',
            name='pict',
            field=models.ImageField(blank=True, default='null', null=True, upload_to='static/publisher_img'),
        ),
    ]
