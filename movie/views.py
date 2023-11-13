from django.shortcuts import render, redirect
from django.http import HttpResponse, HttpResponseRedirect
from .models import Movie, CustomUser, UserFilms, UserWatchList, Friend_Request, Profile
from django.core.paginator import Paginator
from .forms import RegistrationForm
from django.contrib.auth import login, logout, authenticate
from django.contrib.auth.decorators import login_required
import locale 
from django.db.models  import Q
from movie.utils import get_max_order, reorder, get_watchlist_order, reorderWatchList
from django.contrib import messages
from django.urls import reverse
from django_htmx.http import HttpResponseClientRedirect
# Create your views here.

def Home(request):
    return redirect(MovieList)


def SearchUsers(request):
    search_text = request.POST.get('search')
    if search_text:
        results = CustomUser.objects.filter(first_name__icontains=search_text) | CustomUser.objects.filter(last_name__icontains=search_text) | CustomUser.objects.filter(email__startswith=search_text).values() 
    else:
        results=''
    return render(request, 'partials/search-results.html', {'results':results})

def MovieList(request):
    movies = Movie.objects.all().order_by("rank")
    movie_count = movies.count()
    paginator = Paginator(movies,15) #show 15 movies per page
    page_number = request.GET.get("page",1)
    page_obj = paginator.get_page(page_number)

    if request.htmx:
        return render(request, 'partials/default-movies.html', {'movies':page_obj, 'movie_count':movie_count} )
    return render(request, 'movie/movie-list.html', {'movies':page_obj, 'movie_count':movie_count})


def SearchMovies(request):
    q = request.POST.get('movie-search') 
    g = request.GET.get('genre')
    print(g)
    if q:
        movies = Movie.objects.filter(Q(title__icontains=q) | Q(director__icontains=q) | Q(year=q)).order_by("rank")
        movie_count = movies.count()

    elif g:
        movies = Movie.objects.filter(Q(genre_list__icontains=g)).order_by("rank")
        movie_count = movies.count()
    else:
        return MovieList(request)

    return render(request, 'partials/movie-search.html', {"movie_count":movie_count, 'filtered_movies':movies, 'q':q} )

def MovieDetail(request,pk):
    locale.setlocale(locale.LC_ALL, '')
    is_fav = False
    in_watchList = False
    users = CustomUser.objects.all()
    movie = Movie.objects.get(id=pk)
    user=request.user

    if user in users:
        if UserFilms.objects.filter(movie=movie, user=user).exists():
            is_fav = True
        if UserWatchList.objects.filter(movie=movie, user=user).exists():
            in_watchList = True
    context = {'movie':movie, 'favorited':is_fav, 'in_watchlist':in_watchList}

    return render(request,'movie/movie-detail.html', context)

@login_required
def favorite_list(request,pk):

    user = CustomUser.objects.get(id=pk)
    is_owner = True
    movies = UserFilms.objects.filter(user=user)
    if user != request.user:
        is_owner = False
    context={'movies':movies, 'user_profile':user, 'is_owner':is_owner}
    return render(request, 'favorite-list.html', context)


def favorite_add(request,pk):
    if not request.user.is_authenticated:
         return HttpResponseClientRedirect(reverse("login"))
        
    else: 
        movie = Movie.objects.get(id=pk)
        user = request.user
        if not UserFilms.objects.filter(movie=movie, user=user).exists():
            UserFilms.objects.create(movie=movie, 
                                    user=user, 
                                    order=get_max_order(request.user)
                                    )

            messages.success(request, f"You have added '{movie.title}' to your favorites.")

        context = {'movie':movie}
        return render(request, 'partials/add-favorite.html', context)

@login_required
def favorite_remove(request,pk):
    movie = Movie.objects.get(id=pk)
    user = request.user
    if UserFilms.objects.filter(movie=movie, user=user).exists():
        UserFilms.objects.filter(movie=movie, user=user).delete()
        messages.error(request, f"You have removed '{movie.title}' from your favorites.")
        reorder(request.user)
    context = {'movie':movie}
    return render(request, 'partials/remove-favorite.html', context)     



    
@login_required
def watch_list(request, pk):
    is_owner = False
    user = CustomUser.objects.get(id=pk)
    movies = UserWatchList.objects.filter(user=user)
    if user == request.user:
        is_owner = True
    context={'movies':movies, 'user_profile':user, 'is_owner':is_owner}
    return render(request, 'watch-list.html', context)


def watchlist_add(request,pk):
    if not request.user.is_authenticated:
         return HttpResponseClientRedirect(reverse("login"))
    
    else:
        movie = Movie.objects.get(id=pk)
        user = request.user
        if not UserWatchList.objects.filter(movie=movie, user=user).exists():
            UserWatchList.objects.create(movie=movie, 
                                    user=user, 
                                    order=get_watchlist_order(request.user)
                                    )

            messages.success(request, f"You have added '{movie.title}' to your watch list.")

        context = {'movie':movie}
        return render(request, 'partials/add-watchlist.html', context)


@login_required
def watchlist_remove(request,pk):
    movie = Movie.objects.get(id=pk)
    user = request.user
    if UserWatchList.objects.filter(movie=movie, user=user).exists():
        UserWatchList.objects.filter(movie=movie, user=user).delete()
        messages.error(request, f"You have removed '{movie.title}' from your watchlist.")
        reorder(request.user)
    context = {'movie':movie}
    return render(request, 'partials/remove-watchlist.html', context)    


def sign_up(request):
    if request.method == 'POST':
        form = RegistrationForm(request.POST)
        if form.is_valid():
            user=form.save()    
            login(request,user)
            return redirect('home')
    else:
        form = RegistrationForm()

    return render(request, 'registration/sign_up.html', {"form":form})

@login_required
def UserProfile(request,pk):
    user = CustomUser.objects.get(id=pk)
    profile = user.profile
    favorites = UserFilms.objects.filter(user=user)[0:5]
    watchlist = UserWatchList.objects.filter(user=user)[0:5]
    friend_requests = Friend_Request.objects.filter(to_user=request.user)
    friend_request_count = Friend_Request.objects.filter(to_user=request.user).count()
    friend_list = profile.friends.all()
    
    isFriend = False
    if request.user.profile in friend_list:
        isFriend = True
    
    context = {'profile':profile, 'favorites':favorites, 'watchlist':watchlist, 'user':user, 'friend_requests':friend_requests, 'friend_request_count':friend_request_count, 'friend_list':friend_list, 'isFriend':isFriend}
    return render(request, 'profile.html', context)


def sort(request):
    film_pks_order = request.POST.getlist('film_order')
    is_owner = True
    films = []
    for idx, film_pk in enumerate(film_pks_order, start=1):
        userfilm = UserFilms.objects.get(id=film_pk)
        
        if userfilm.user != request.user:
            is_owner = False
            return
        userfilm.order = idx
        userfilm.save()
        films.append(userfilm)
    print(is_owner)
    return render(request, 'partials/movie-list.html', {'movies':films, 'is_owner':is_owner})



def sortWatchList(request):
    film_pks_order = request.POST.getlist('film_order')
    print(film_pks_order)
    films = []
    for idx, film_pk in enumerate(film_pks_order, start=1):
        userfilm = UserWatchList.objects.get(id=film_pk)
        
        userfilm.order = idx
        userfilm.save()
        films.append(userfilm)
        
    return render(request, 'partials/watch-list-partial.html', {'movies':films})



def send_friend_request(request,pk):
    from_user = request.user
    
    to_user = CustomUser.objects.get(id=pk)

    friend_request,created = Friend_Request.objects.get_or_create(from_user=from_user, to_user=to_user)

    if created:
        messages.success(request, f"You have sent '{to_user.email}' a friend request.")
    else:
        messages.error(request, f"You have already sent this person a friend request.")

    return HttpResponseRedirect(request.META['HTTP_REFERER'])


def remove_friend(request,pk):
    user_profile = Profile.objects.get(user=request.user)
    friend_profile = Profile.objects.get(user=pk)
  
    if user_profile in friend_profile.friends.all() and friend_profile in user_profile.friends.all():
        user_profile.friends.remove(friend_profile)
        friend_profile.friends.remove(user_profile)
        print('removed')
        messages.success(request, f"You have removed '{friend_profile}' from your friends.")

    else:
        messages.error(request, f"An error occurred. Please try again.")

    return HttpResponseRedirect(request.META['HTTP_REFERER'])



def accept_friend_request(request,pk):
    friend_request = Friend_Request.objects.get(id=pk)
    if friend_request.to_user == request.user:
        user_profile = Profile.objects.get(user=friend_request.to_user)
        sender_profile = Profile.objects.get(user=friend_request.from_user)
        user_profile.friends.add(sender_profile)
        sender_profile.friends.add(user_profile)
        friend_request.delete()
        messages.success(request, f"You have accepted '{sender_profile.user.first_name}'  friend request.")

    else:
      messages.success(request, f"You have rejected '{sender_profile.user.email}'  friend request.")
    return HttpResponseRedirect(request.META['HTTP_REFERER'])
