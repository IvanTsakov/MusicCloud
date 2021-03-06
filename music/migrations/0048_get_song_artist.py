# -*- coding: utf-8 -*-
# Generated by Django 1.11.9 on 2018-03-14 12:42
from __future__ import unicode_literals

from django.db import migrations

def get_song_artist(apps, schema_editor):
	Song = apps.get_model('music', 'Song')
	Artist = apps.get_model('music', 'Artist')
	for song in Song.objects.all():
		if song.album.album_title == 'Master of the Puppets':
			artist = Artist.objects.get(name='Metallica')
			song.artist = artist
			song.save()
		if song.album.album_title == 'Appetite for Destruction':
			artist = Artist.objects.get(name='Guns N Roses')
			song.artist = artist
			song.save()
		if song.album.album_title == 'Number Ones':
			artist = Artist.objects.get(name='Michael Jackson')
			song.artist = artist
			song.save()
		if song.album.album_title == 'Kind of Blue':
			artist = Artist.objects.get(name='Miles Davis')
			song.artist = artist
			song.save()
		if song.album.album_title == 'The Eminem Show':
			artist = Artist.objects.get(name='Eminem')
			song.artist = artist
			song.save()

class Migration(migrations.Migration):

    dependencies = [
        ('music', '0047_song_artist'),
    ]

    operations = [
    	migrations.RunPython(get_song_artist)
    ]
