# Generated by Django 4.2.1 on 2023-07-30 04:59

from django.conf import settings
from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('movie', '0005_movie_watch_list_profile_watch_list'),
    ]

    operations = [
        migrations.CreateModel(
            name='UserFilms',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('order', models.PositiveSmallIntegerField()),
                ('movie', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='movie.movie')),
                ('user', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to=settings.AUTH_USER_MODEL)),
            ],
            options={
                'ordering': ['order'],
            },
        ),
    ]