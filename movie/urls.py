from django.contrib import admin
from django.urls import path
from .views import MovieList, MovieDetail, sign_up, UserProfile, favorite_add, favorite_remove, favorite_list, watchlist_add, watchlist_remove, watch_list, sort, sortWatchList, SearchUsers, SearchMovies,send_friend_request, accept_friend_request, remove_friend

urlpatterns = [
path('movie-list', MovieList, name='movie-list'),
path('movie-list/<int:pk>', MovieDetail, name='movie-detail'),
path('search-users', SearchUsers, name='search-users'),
path('search-movies', SearchMovies, name='search-movies'),
path('fav/<int:pk>', favorite_add, name='favorite-add'),
path('fav-remove/<int:pk>', favorite_remove, name='favorite-remove'),
path('watch/<int:pk>', watchlist_add, name='watchlist-add'),
path('watch-remove/<int:pk>', watchlist_remove, name='watchlist-remove'),
path('favorite-list/<int:pk>', favorite_list , name='favorite-list'),
path('watch-list/<int:pk>', watch_list , name='watch-list'),
path('sign-up', sign_up, name='sign_up'),
path('profile/<str:pk>', UserProfile, name='profile'),
path('send_friend_request/<int:pk>', send_friend_request, name='send-friend-request'),
path('remove_friend/<int:pk>', remove_friend, name='remove-friend'),
path('accept_friend_request/<int:pk>', accept_friend_request, name='accept-friend-request')
]

htmx_urlpatterns = [
    path('sort', sort, name='sort'),
    path('sortWatchList', sortWatchList, name='sort-watch'),

]

urlpatterns += htmx_urlpatterns