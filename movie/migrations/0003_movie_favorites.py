# Generated by Django 4.2.1 on 2023-07-22 20:05

from django.conf import settings
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('movie', '0002_alter_movie_audience_rating'),
    ]

    operations = [
        migrations.AddField(
            model_name='movie',
            name='favorites',
            field=models.ManyToManyField(blank=True, default=None, related_name='favorite', to=settings.AUTH_USER_MODEL),
        ),
    ]