from django.contrib.auth.models import User
from django import forms
from models import Album, Song


class UserForm(forms.ModelForm):
	password = forms.CharField(widget = forms.PasswordInput)
	class Meta:
		model = User
		fields = ['username', 'email', 'password']

class AlbumForm(forms.ModelForm):
	class Meta:
		model = Album
		fields = ['artist', 'album_title', 'genre', 'album_logo']
	def __init__(self, *args, **kwargs):
		creator = kwargs.pop('creator')
		super(AlbumForm, self).__init__(*args, **kwargs)
		self.instance.creator = creator

class SongForm(forms.ModelForm):
	class Meta:
		model = Song
		fields = ['album', 'song_title']

	def __init__(self, *args, **kwargs):
		album_creator=kwargs.pop('album_creator')
		super(SongForm, self).__init__(*args, **kwargs)
		self.instance.album_creator = album_creator
		self.instance.file_type = 'mp3'

class AlbumSongForm(forms.ModelForm):
	class Meta:
		model = Song
		fields = ['song_title']

	def __init__(self, *args, **kwargs):
		album = kwargs.pop('album')
		creator=kwargs.pop('creator')
		super(AlbumSongForm, self).__init__(*args, **kwargs)
		self.instance.album = album
		self.instance.creator = creator
		self.instance.file_type = 'mp3'

