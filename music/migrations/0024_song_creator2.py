# -*- coding: utf-8 -*-
# Generated by Django 1.11.9 on 2018-03-02 10:27
from __future__ import unicode_literals

from django.conf import settings
from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
        ('music', '0023_auto_20180301_1505'),
    ]

    operations = [
        migrations.AddField(
            model_name='song',
            name='creator2',
            field=models.ForeignKey(null=True, on_delete=django.db.models.deletion.CASCADE, related_name='song_creator', to=settings.AUTH_USER_MODEL),
        ),
    ]
