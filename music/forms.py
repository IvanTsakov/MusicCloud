from django.contrib.auth.models import User
from django import forms
from models import Album, Song, Comment
from django.contrib.auth.forms import UserCreationForm


class SignUp_UserForm(forms.ModelForm):
	first_name = forms.CharField(max_length=30, help_text='Enter your firsts name')
	last_name = forms.CharField(max_length=30, help_text='Enter your last name')
	password = forms.CharField(widget = forms.PasswordInput)
	class Meta:
		model = User
		fields= ['username', 'first_name', 'last_name', 'email','password']


class Registration_UserForm(forms.ModelForm):
	password = forms.CharField(widget = forms.PasswordInput)
	class Meta:
		model = User
		fields = ['username', 'email', 'password', 'first_name', 'last_name']

class AlbumForm(forms.ModelForm):
	class Meta:
		model = Album
		fields = ['album_title','album_logo']
	def __init__(self, *args, **kwargs):
		creator = kwargs.pop('creator')
		super(AlbumForm, self).__init__(*args, **kwargs)
		self.instance.creator = creator

class SongForm(forms.ModelForm):
	class Meta:
		model = Song
		fields = ['album', 'song_title', 'genre','artist', 'tempo']

	def __init__(self, *args, **kwargs):
		creator=kwargs.pop('creator')
		super(SongForm, self).__init__(*args, **kwargs)
		self.instance.creator = creator

class AlbumSongForm(forms.ModelForm):
	class Meta:
		model = Song
		fields = ['song_title', 'genre', 'artist', 'tempo']

	def __init__(self, *args, **kwargs):
		album = kwargs.pop('album')
		creator=kwargs.pop('creator')
		super(AlbumSongForm, self).__init__(*args, **kwargs)
		self.instance.album = album
		self.instance.creator = creator

class CommentForm(forms.ModelForm):

    class Meta:
        model = Comment
        fields = ('text',)

    def __init__(self, *args, **kwargs):
    	author = kwargs.pop('author')
    	super(CommentForm, self).__init__(*args, **kwargs)
    	self.instance.author = author

