# -*- coding: utf-8 -*-
# Generated by Django 1.11.9 on 2018-03-13 09:39
from __future__ import unicode_literals

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('music', '0037_auto_20180308_1045'),
    ]

    operations = [
        migrations.AddField(
            model_name='song',
            name='genre',
            field=models.CharField(choices=[(1, 'Rock'), (2, 'Hip-hop'), (3, 'Pop'), (4, 'Metal'), (5, 'Jazz')], default=0, max_length=50),
            preserve_default=False,
        ),
    ]