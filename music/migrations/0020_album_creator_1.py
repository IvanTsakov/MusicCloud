# -*- coding: utf-8 -*-
# Generated by Django 1.11.9 on 2018-03-01 14:47
from __future__ import unicode_literals

from django.db import migrations
from django.contrib.auth.models import User

def change_creator(apps, schema_editor):
    Album = apps.get_model('music', 'Album')
    for album in Album.objects.all():
        creator, created = User.objects.get_or_create(username = album.creator)
        # album.album_creator = creator
        album.save()

class Migration(migrations.Migration):

    dependencies = [
        ('music', '0017_album_album_creator'),
    ]

    operations = [
    	migrations.RunPython(change_creator)
    ]