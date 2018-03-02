# -*- coding: utf-8 -*-
from __future__ import unicode_literals
from django.utils.encoding import python_2_unicode_compatible
from django.db import models
from django.core.urlresolvers import reverse
from django.contrib.auth.models import User

@python_2_unicode_compatible
class Album(models.Model):
	artist = models.CharField(max_length=250)
	album_title = models.CharField(max_length=250)
	genre = models.CharField(max_length=100)
	album_logo = models.FileField() 
	creator = models.ForeignKey(User, null = True, related_name = "album_creator")
	users = models.ManyToManyField(User)

	def get_absolute_url(self):
		return reverse('music:detail', kwargs={'pk' : self.pk})

	def __str__(self):
		return self.album_title + ' - ' + self.artist

		
@python_2_unicode_compatible
class Song(models.Model):
	album = models.ForeignKey(Album, on_delete = models.CASCADE)
	file_type = models.CharField(max_length=10)
	song_title = models.CharField(max_length=5)
	creator = models.CharField(max_length=200)
	users = models.ManyToManyField(User)

	def get_absolute_url(self):
		return reverse('music:detail', kwargs={'pk' : self.album.pk})

	def __str__(self):
		return self.song_title
