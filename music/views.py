from django.views import generic 
from django.views.generic.edit import CreateView, UpdateView, DeleteView
from django.views.decorators.csrf import csrf_protect
from django.core.urlresolvers import reverse_lazy, reverse
from django.shortcuts import render, redirect, get_object_or_404, render_to_response
from django.contrib import messages, auth
from django.contrib.auth import authenticate, logout as auth_logout, login as auth_login, get_user_model
from django.contrib.auth.models import User
from django.contrib.auth.decorators import login_required
from django.views.generic import View
from music.models import Album, Song, Artist
from music.forms import Registration_UserForm, AlbumSongForm, AlbumForm, SongForm,SignUp_UserForm, CommentForm
from music.choices import GENRE_CHOICES
from django import forms
from django.http import QueryDict, HttpResponseRedirect
from django.db.models import Count, Q, CharField, Case, Value, When, F, BooleanField
from copy import copy
from django.core.paginator import Paginator, EmptyPage, PageNotAnInteger
from itertools import chain
import operator

@login_required
def index_view(request):
    albums = Album.objects.all()
    context_object_name = 'all_albums'
    user_favorite_albums = request.user.album_set.all()

    for album in albums:
         album.is_favorite = album in user_favorite_albums

    return render(request,'music/index.html', {
        'albums':albums,
        })

def detail_view(request, pk):
    album = get_object_or_404(Album, pk= pk)
    songs = album.song_set.all()
    user_favorite_songs = request.user.song_set.all()
    for song in songs:
        song.is_favorite = song in user_favorite_songs
    return render(request,'music/detail.html', {'album':album, 'songs':songs})   

def song_view(request, pk):
    song = get_object_or_404(Song, pk=pk)
    user = request.user
        
    initials = user.profile.get_initials()
    if request.method == "POST":
        form = CommentForm(request.POST, author = user)
        if form.is_valid():
            comment = form.save(commit=False)
            comment.song = song
            comment.save()
            return redirect('music:song_view', pk=pk)
    else:
        form = CommentForm(author = user)
    
    comments = song.comment_set.all().order_by('-created_date')
    return render(request,'music/song.html', {
        'song':song, 
        'initials': initials, 
        'form':form,
        'comments': comments 
    }) 

@login_required
def songs_view(request):
    all_songs = Song.objects.all()

    filters_map = {
        'tempo': {
            'slow': {'tempo__lt': 90},
            'medium': {'tempo__range': (90, 120)},
            'fast': {'tempo__gt': 120},
        },
        'genre': {
            'rock': {'genre': 1},
            'hiphop': {'genre': 2},
            'pop': {'genre': 3},
            'metal': {'genre': 4},
            'jazz': {'genre': 5},
        }
    }

    genre_dict = dict(GENRE_CHOICES)

    genre_title_map = {
        'rock': genre_dict[1],
        'hiphop': genre_dict[2],
        'pop': genre_dict[3],
        'metal': genre_dict[4],
        'jazz': genre_dict[5],
    }

    def apply_filters(qs, filters):
        for k,v in filters.iteritems():
            qs = qs.filter(**filters_map[k][v])
        return qs

    from collections import OrderedDict

    order_fields = OrderedDict([
        ('artist__name', {
            '': ('artist__name', ''),
            'artist__name': ('-artist__name', 'up'),
            '-artist__name': ('', 'down'),
        }),
        ('song_title', {
            '': ('song_title', ''),
            'song_title': ('-song_title', 'up'),
            '-song_title': ('', 'down'),
            }),
        ('tempo', {
            '': ('tempo', ''),
            'tempo': ('-tempo', 'up'),
            '-tempo': ('', 'down'),
            }),
        ('genre', {
            '': ('genre', ''),
            'genre': ('-genre', 'up'),
            '-genre': ('', 'down'),
            }),
    ])

    order = request.GET.get('order', 'id')
    orders = []
    for o_field in order_fields.keys():
        if order in order_fields[o_field]:
            order_field, order_direction = order_fields[o_field][order]
            orders.append({
                    'order': order_direction,
                    'order_title': o_field.replace('_', ' ').title(),
                    'order_field': order_field
                })
        else:
            orders.append({
                    'order': '',
                    'order_title': o_field.replace('_', ' ').title(),
                    'order_field': o_field
                })


    def apply_order(qs, order):
        if order:
            return qs.order_by(order)
        return qs.order_by('id')

    filter_names = {'tempo', 'genre'}
##  
    def get_filters(get):
        return {k:v for k,v in get.iteritems() if v and k in filter_names}

    filters = get_filters(request.GET)
    songs = apply_filters(all_songs, filters)

    songs = apply_order(songs, order)

    filters_wo_genre = copy(filters)
    filters_wo_genre.pop('genre', None)
    genre_filters = apply_filters(all_songs, filters_wo_genre).annotate(
        genre_title = Case(
            When((Q(genre = 1)), then=Value('rock')),
            When((Q(genre = 2)), then=Value('hiphop')),
            When((Q(genre = 3)), then=Value('pop')),
            When((Q(genre = 4)), then=Value('metal')),
            When((Q(genre = 5)), then=Value('jazz')),
            output_field = CharField()
        )).values('genre_title').annotate(cnt=Count('pk')).values('genre_title', 'cnt').order_by('cnt')
    for f in genre_filters:
        f['title'] = genre_title_map[f['genre_title']]

    filters_wo_tempo = copy(filters)
    filters_wo_tempo.pop('tempo', None)
    tempo_filters = apply_filters(all_songs, filters_wo_tempo).annotate(
        tempo_speed=Case(
            When((Q(tempo__lt = 90)), then=Value('slow')),
            When((Q(tempo__range=(90, 120))), then=Value('medium')),
            When((Q(tempo__gt = 120)), then=Value('fast')),
            output_field = CharField()
        )).values('tempo_speed').annotate(cnt=Count('pk')).values('tempo_speed', 'cnt').order_by('cnt')
    for f in tempo_filters:
        f['title'] = f['tempo_speed'].title()

    paginator = Paginator(songs, 15)
    page = request.GET.get('page')

    try:
        song_paginator = paginator.page(page)
    except PageNotAnInteger:
        song_paginator = paginator.page(1)
    except EmptyPage:
        song_paginator = paginator.page(paginator.num_pages)

    filters_get = QueryDict(mutable=True)
    filters_get.update(request.GET.dict())

    if request.GET.get('order') == order:
        filters_get.pop('order')

    return render(request,'music/songs.html', {
        'song_paginator':song_paginator,
        'genres' : genre_filters ,
        'tempos' : tempo_filters ,
        'orders' : orders,
        'artists': Artist.objects.all(),
        'filters_get': filters_get,
   }) 
    
def album_create(request):
    user = request.user
    template_name = 'music/index.html'
    if request.method == 'POST':
        form = AlbumForm(request.POST, request.FILES, creator=user)
        if form.is_valid():
            album = form.save()
            return redirect('music:index')
    else:
        form = AlbumForm(creator=user)
    return render(request, 'music/album_form.html', {
        'creator':user,
        'form':form
    }) 


def album_update(request, pk):
    user = request.user
    album =get_object_or_404(Album, pk=pk)
    if user!=album.creator:
        messages.add_message(request, messages.INFO, 'You cannot update this album, because you are not the creator.')
        return redirect('music:index')
    else:
        if request.POST:
            form = AlbumForm(request.POST, request.FILES,instance = album, creator = album.creator)
            if form.is_valid():
                form.save()
                return redirect('music:index')
        form = AlbumForm(instance = album, creator=album.creator)
        return render(request, 'music/album_form.html', {
        'creator':user,
        'form':form
    }) 

class AlbumDelete(DeleteView):
    model = Album
    success_url = reverse_lazy('music:index')

def song_create(request):
    user = request.user
    template_name = 'music/songs.html'
    if request.method == 'POST':
        form = SongForm(request.POST,creator=user)
        if form.is_valid():
            song = form.save()
            return redirect('music:songs')
    else:
        form = SongForm(creator=user)
    return render(request, 'music/song_form.html', {
        'creator':user,
        'form':form
    }) 

def album_song_create(request, pk):
    album = Album.objects.get(pk=pk)
    user = request.user
    if request.method == 'POST':
        form = AlbumSongForm(request.POST, album=album, creator = user)
        if form.is_valid():
            song = form.save()
            return redirect(album)
    else:
        form = AlbumSongForm(album=album, creator=user)

    return render(request, 'music/song_form.html', {
        'album':album,
        'form':form
    }) 

def song_update(request, pk):
    user = request.user
    song = get_object_or_404(Song, pk=pk)
    if user!=song.creator:
        messages.add_message(request, messages.INFO, 'You cannot update this song, because you are not the creator.')
        return redirect('music:songs')
    else:
        if request.POST:
            form = SongForm(request.POST,instance = song, creator= song.creator)
            if form.is_valid():
                form.save()
                return redirect('music:songs')
        form = SongForm(instance = song, creator=song.creator)
        return render(request, 'music/song_form.html', {
        'creator':user,
        'form':form
    }) 

def delete_song(request, pk):
    song = get_object_or_404(Song, pk = pk)
    album = get_object_or_404(Album, pk = song.album.pk)
    song.delete()
    return redirect(album)

def delete_song_in_songs(request, pk):
    song = get_object_or_404(Song, pk = pk)
    song.delete()
    return redirect('music:songs')


def favorite_album(request, pk):
    user = request.user
    album = get_object_or_404(Album, pk = pk)
    if album in user.album_set.all():
        user.album_set.remove(album)
    else:
        user.album_set.add(album)
    return redirect('music:index')

def favorite_song(request, pk):
    user = request.user
    song = get_object_or_404(Song, pk=pk)
    album = get_object_or_404(Album, pk = song.album.pk)
    if song in user.song_set.all():
        user.song_set.remove(song)
    else:
        user.song_set.add(song)
    return redirect(album)

def favorite_song_in_songs(request, pk):
    user = request.user
    song = get_object_or_404(Song, pk=pk)
    if song in user.song_set.all():
        user.song_set.remove(song)
    else:
        user.song_set.add(song)
    return redirect('music:songs')

def favorited_songs(request):
    user = request.user
    songs = user.song_set.all()
    return render(request,'music/favorite-songs.html', {'songs':songs})


def favorited_albums(request):
    user = request.user
    albums = user.album_set.all()

    return render(request,'music/favorite-albums.html', {'albums':albums})


class UserFormView(View):
    form_class = Registration_UserForm
    template_name = 'music/registration_form.html'

    def get(self, request):
        form = self.form_class(None)
        return render(request, self.template_name, {'form':form})

    def post(self, request):
        form = self.form_class(request.POST)

        if form.is_valid():
            user = form.save(commit=False)

            username = form.cleaned_data['username']
            password = form.cleaned_data['password']
            user.set_password(password)
            user.save()
            user = authenticate(username=username, password=password)

            if user is not None:
                if user.is_active:
                    auth_login(request, user)
                    return redirect('music:index')  

        return render(request, self.template_name, {'form':form})



def login(request):
    c={}
    return render(request,'login.html',{'c':c})

def auth(request):

    username = request.POST.get('username', '')
    password = request.POST.get('password', '')
    user = authenticate(request, username=username, password=password)

    if user is not None:
        auth_login(request,user)
        return redirect('music:index')
    else:
        return render(request,'music/login.html')

def logout(request):
    auth_logout(request)
    return render(request,'music/login.html')


def all_users(request):
    users = User.objects.annotate(num_albums = Count('song')).order_by('-num_albums')
    return render(request, 'music/users.html', {'users' : users})

def search(request):

    search = request.GET.get('q')

    if search:
        songs = Song.objects.filter(Q(song_title__icontains = search)).distinct()
        artists = Artist.objects.filter(Q(name__icontains = search)).distinct()

    results = sorted(chain(songs, artists), key = lambda x: x.compare(search), reverse = True)

    page = request.GET.get('page',1)
    paginator = Paginator(results, 20)

    try:
        results_paginator = paginator.page(page)
    except PageNotAnInteger:
        results_paginator = paginator.page(1)

    return render(request, 'music/search.html', {
        'results_paginator':results_paginator,  
        'search':search,
        'paginator':paginator,
        })

