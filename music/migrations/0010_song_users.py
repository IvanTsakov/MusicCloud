# -*- coding: utf-8 -*-
# Generated by Django 1.11.9 on 2018-02-22 14:21
from __future__ import unicode_literals

from django.conf import settings
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
        ('music', '0009_song_creator'),
    ]

    operations = [
        migrations.AddField(
            model_name='song',
            name='users',
            field=models.ManyToManyField(to=settings.AUTH_USER_MODEL),
        ),
    ]
