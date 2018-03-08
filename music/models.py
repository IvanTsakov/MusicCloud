# -*- coding: utf-8 -*-
from __future__ import unicode_literals
from django.utils.encoding import python_2_unicode_compatible
from django.db import models
from django.core.urlresolvers import reverse
from django.contrib.auth.models import User
from django.utils import timezone
from django.db.models.signals import post_save
from django.dispatch import receiver

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
	song_title = models.CharField(max_length=200)
	creator = models.ForeignKey(User, related_name = "creator")
	users = models.ManyToManyField(User)

	def get_absolute_url(self):
		return reverse('music:detail', kwargs={'pk' : self.album.pk})

	def __str__(self):
		return self.song_title


class Profile(models.Model):
	user = models.OneToOneField(User, on_delete = models.CASCADE)

	def get_initials(self):
		if self.user.first_name and self.user.last_name:
			first_letter = self.user.first_name[0]
			second_letter = self.user.last_name[0]
			initials = first_letter + second_letter
			return initials
		else:
			first_letter = self.user.username[0]
			second_letter = self.user.username[1]
			initials = first_letter + second_letter
			return initials

def create_user_profile(sender, instance, created, **kwargs):
    if created:
        Profile.objects.create(user=instance)

post_save.connect(create_user_profile, sender=User)

class Comment(models.Model):
	author = models.ForeignKey(User)
	song = models.ForeignKey(Song)
	text = models.TextField()
	created_date = models.DateTimeField(default=timezone.now)

