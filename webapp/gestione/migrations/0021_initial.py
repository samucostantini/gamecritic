# Generated by Django 4.2.5 on 2023-10-09 08:57

from django.conf import settings
import django.core.validators
from django.db import migrations, models
import django.db.models.deletion
import django_countries.fields


class Migration(migrations.Migration):

    initial = True

    dependencies = [
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
        ('gestione', '0020_remove_player_games_remove_player_user_and_more'),
    ]

    operations = [
        migrations.CreateModel(
            name='Game',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('titolo', models.CharField(max_length=100)),
                ('price', models.IntegerField()),
                ('category', models.CharField(max_length=20)),
                ('age', models.IntegerField()),
                ('pict', models.ImageField(blank=True, default='null', null=True, upload_to='static/game_img')),
                ('description', models.TextField()),
                ('console', models.CharField(choices=[('switch', 'Switch'), ('ds', 'DS'), ('ps1', 'PS1'), ('ps2', 'PS2')], max_length=20)),
            ],
        ),
        migrations.CreateModel(
            name='Player',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('name', models.CharField(max_length=100)),
                ('surname', models.CharField(max_length=100)),
                ('age', models.PositiveIntegerField()),
                ('pict', models.ImageField(blank=True, default='null', null=True, upload_to='static/player_img')),
                ('console', models.CharField(choices=[('switch', 'Nintendo Switch'), ('ps', 'PlayStation'), ('xbox', 'Xbox')], max_length=10)),
                ('country', django_countries.fields.CountryField(max_length=2)),
                ('games', models.ManyToManyField(to='gestione.game')),
                ('user', models.OneToOneField(on_delete=django.db.models.deletion.CASCADE, to=settings.AUTH_USER_MODEL)),
            ],
        ),
        migrations.CreateModel(
            name='Publisher',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('name', models.CharField(max_length=100)),
                ('website', models.CharField(max_length=100)),
                ('pict', models.ImageField(upload_to='publisher_img')),
                ('user', models.OneToOneField(on_delete=django.db.models.deletion.CASCADE, to=settings.AUTH_USER_MODEL)),
            ],
        ),
        migrations.AddField(
            model_name='game',
            name='publisher',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='gestione.publisher'),
        ),
        migrations.CreateModel(
            name='Review',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('plot_rating', models.PositiveIntegerField(default=1, validators=[django.core.validators.MinValueValidator(1), django.core.validators.MaxValueValidator(5)])),
                ('music_rating', models.PositiveIntegerField(default=1, validators=[django.core.validators.MinValueValidator(1), django.core.validators.MaxValueValidator(5)])),
                ('gameplay_rating', models.PositiveIntegerField(default=1, validators=[django.core.validators.MinValueValidator(1), django.core.validators.MaxValueValidator(5)])),
                ('performance_rating', models.PositiveIntegerField(default=1, validators=[django.core.validators.MinValueValidator(1), django.core.validators.MaxValueValidator(5)])),
                ('comment', models.TextField()),
                ('game', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='gestione.game')),
                ('player', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='gestione.player')),
            ],
            options={
                'unique_together': {('game', 'player')},
            },
        ),
    ]
