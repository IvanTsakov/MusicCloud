# -*- coding: utf-8 -*-
# Generated by Django 1.11.9 on 2018-03-15 10:36
from __future__ import unicode_literals

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('music', '0051_song_tempo'),
    ]

    operations = [
        migrations.AlterField(
            model_name='song',
            name='tempo',
            field=models.IntegerField(),
        ),
    ]
