from django.contrib import admin

# Register your models here.
from .models import Movie, CustomUser, Profile,  UserFilms, UserWatchList, Friend_Request

admin.site.register(Movie)
admin.site.register(CustomUser)
admin.site.register(Profile)
admin.site.register(UserFilms)
admin.site.register(UserWatchList)
admin.site.register(Friend_Request)