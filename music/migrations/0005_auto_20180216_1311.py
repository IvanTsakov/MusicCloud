# -*- coding: utf-8 -*-
# Generated by Django 1.11.9 on 2018-02-16 13:11
from __future__ import unicode_literals

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('music', '0004_auto_20180216_1310'),
    ]

    operations = [
        migrations.RenameField(
            model_name='album',
            old_name='logo',
            new_name='album_logo',
        ),
        migrations.RenameField(
            model_name='album',
            old_name='title',
            new_name='album_title',
        ),
    ]
