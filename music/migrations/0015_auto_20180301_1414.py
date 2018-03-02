# -*- coding: utf-8 -*-
# Generated by Django 1.11.9 on 2018-03-01 14:14
from __future__ import unicode_literals

from django.db import migrations
from django.db import models
from django.contrib.auth.models import User


def change_creator(apps, schema_editor):

	Album = apps.get_model('music', 'Album')
	# User = apps.get_model('music', 'User')
	for album in Album.objects.all():
		for user in User.objects.all():
			if album.creator == user.username:
				album.creator = models.ForeignKey(User)
				album.save()
			else:
				continue

class Migration(migrations.Migration):

    dependencies = [
        ('music', '0014_auto_20180301_1244'),
    ]

    operations = [
    	migrations.RunPython(change_creator)
    ]