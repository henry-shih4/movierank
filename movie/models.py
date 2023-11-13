from django.db import models
from django.utils.translation import gettext as _
from django.contrib.auth.models import AbstractUser
from .managers import CustomUserManager
from django.contrib.postgres.fields import ArrayField
from django.db.models.signals import post_save
from django.dispatch import receiver


# Create your models here.

class CustomUser(AbstractUser):
    username = None
    email = models.EmailField(_("email address"), unique=True)

    USERNAME_FIELD = "email"
    REQUIRED_FIELDS = []

    objects = CustomUserManager()

    def __str__(self):
        return self.email
    
class Movie(models.Model):
    title = models.CharField(_("title"), max_length=255)
    year = models.CharField(_("year"), max_length=4)
    director = models.CharField(_("director"), max_length=255)
    rank = models.PositiveSmallIntegerField(_("rank"), default ='0', null=True)
    rating = models.FloatField(_("rating"), null=True)
    votes = models.BigIntegerField(_("votes"), null=True)
    runtime =  models.CharField(_("runtime"), max_length=15, null = True)
    release_date = models.DateField(_("release_date"), null = True)
    poster_img = models.URLField(_("poster_img"), null = True)
    imdb_page = models.URLField(_("imdb_page"), null = True)
    audience_rating = models.CharField(_("audience_rating"), max_length=10, null = True)
    metascore = models.IntegerField(_("metascore"), null = True)
    genre_list = models.CharField(_("genre_list"), max_length = 255, null = True)
    description = models.CharField(_("description"), max_length = 500, null = True) 
    country_of_origin = models.CharField(_("country"),max_length=10, null = True)
    us_canada_gross = models.BigIntegerField(_("us_canada_gross"), null = True)
    worldwide_gross = models.BigIntegerField(_("world_gross"), null = True)
    oscar_nominations = models.IntegerField(_("oscar_nominations"), null = True)
    oscar_wins = models.IntegerField(_("oscar_wins"), null = True)
    cast_list = models.CharField(_("cast_list"), max_length = 500, null = True)

    def __str__(self):
        return self.title
    
    
class Profile(models.Model):
    user = models.OneToOneField(CustomUser, unique=True, null=True, on_delete=models.CASCADE)
    friends = models.ManyToManyField("self")

    def __str__(self):
        return self.user.email
    
class Friend_Request(models.Model):
    from_user = models.ForeignKey(CustomUser, related_name='from_user', on_delete=models.CASCADE)
    to_user = models.ForeignKey(CustomUser, related_name='to_user', on_delete=models.CASCADE)

    def __str__(self):
        return f'{self.from_user.email} to {self.to_user.email}'

class UserFilms(models.Model):
    user = models.ForeignKey(CustomUser, on_delete=models.CASCADE)
    movie = models.ForeignKey(Movie, on_delete=models.CASCADE)
    order = models.PositiveSmallIntegerField()

    class Meta:
        ordering = ['order']

class UserWatchList(models.Model):
    user = models.ForeignKey(CustomUser, on_delete=models.CASCADE)
    movie = models.ForeignKey(Movie, on_delete=models.CASCADE)
    order = models.PositiveSmallIntegerField()

    class Meta:
        ordering = ['order']    

@receiver(post_save, sender=CustomUser)
def create_profile(sender,instance,created,**kwargs):
    if created:
        user_profile = Profile(user=instance)
        user_profile.save()
        
