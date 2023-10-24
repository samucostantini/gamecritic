# Generated by Django 4.2.5 on 2023-10-09 08:57

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('gestione', '0019_rename_title_game_titolo'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='player',
            name='games',
        ),
        migrations.RemoveField(
            model_name='player',
            name='user',
        ),
        migrations.RemoveField(
            model_name='publisher',
            name='user',
        ),
        migrations.AlterUniqueTogether(
            name='review',
            unique_together=None,
        ),
        migrations.RemoveField(
            model_name='review',
            name='game',
        ),
        migrations.RemoveField(
            model_name='review',
            name='player',
        ),
        migrations.DeleteModel(
            name='Game',
        ),
        migrations.DeleteModel(
            name='Player',
        ),
        migrations.DeleteModel(
            name='Publisher',
        ),
        migrations.DeleteModel(
            name='Review',
        ),
    ]
