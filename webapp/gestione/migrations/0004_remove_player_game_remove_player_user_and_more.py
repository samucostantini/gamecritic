# Generated by Django 4.2.5 on 2023-09-22 15:32

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('gestione', '0003_initial'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='player',
            name='game',
        ),
        migrations.RemoveField(
            model_name='player',
            name='user',
        ),
        migrations.RemoveField(
            model_name='publisher',
            name='user',
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
    ]
