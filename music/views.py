from django.views import generic 
from django.views.generic.edit import CreateView, UpdateView, DeleteView
from django.core.urlresolvers import reverse_lazy, reverse
from django.shortcuts import render, redirect, get_object_or_404, render_to_response
from django.contrib.auth import authenticate, logout as auth_logout, login as auth_login, get_user_model
from django.views.generic import View
from music.models import Album, Song
from music.forms import Registration_UserForm, AlbumSongForm, AlbumForm, SongForm,SignUp_UserForm, CommentForm
from django import forms
from django.http import HttpResponseRedirect
from django.contrib import messages, auth
from django.views.decorators.csrf import csrf_protect
from django.contrib.auth.decorators import login_required
from django.db.models import Count
import operator
from django.contrib.auth.models import User

@login_required
def index_view(request):
    albums = Album.objects.all()
    context_object_name = 'all_albums'
    user_favorite_albums = request.user.album_set.all()
    for album in albums:
         album.is_favorite = album in user_favorite_albums
    return render(request,'music/index.html', {'albums':albums})

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
    # if user.first_name and user.last_name:
    #     initials = user.first_name[0] + user.last_name[0]
    # else:
    #     initials = user.username[0] + user.username[1]
        
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
    return render(request,'music/song.html', {'song':song, 'initials': initials, 'form':form}) 

@login_required
def songs_view(request):
    songs = Song.objects.all()
    user_favorite_songs = request.user.song_set.all()
    for song in songs:
        song.is_favorite = song in user_favorite_songs
    return render(request,'music/songs.html', {'songs':songs}) 

    
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
    users = User.objects.annotate(num_albums = Count('album')).order_by('-num_albums')
    return render(request, 'music/users.html', {'users' : users})
