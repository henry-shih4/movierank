# Generated by Django 4.2.1 on 2023-07-30 05:01

from django.conf import settings
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('movie', '0006_userfilms'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='movie',
            name='favorites',
        ),
        migrations.AddField(
    model_name='movie',
    name='favorites',
 field=models.ManyToManyField(blank=True, default=None, related_name='favorite', through='movie.UserFilms', to=settings.AUTH_USER_MODEL),
)
    ]


           
