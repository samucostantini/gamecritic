# Generated by Django 4.2.5 on 2023-10-08 08:56

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('gestione', '0018_rename_titolo_game_title'),
    ]

    operations = [
        migrations.RenameField(
            model_name='game',
            old_name='title',
            new_name='titolo',
        ),
    ]
