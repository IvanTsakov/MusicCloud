# -*- coding: utf-8 -*-
# Generated by Django 1.11.9 on 2018-02-16 13:13
from __future__ import unicode_literals

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('music', '0005_auto_20180216_1311'),
    ]

    operations = [
        migrations.AddField(
            model_name='album',
            name='creator',
            field=models.CharField(default=0, max_length=200),
            preserve_default=False,
        ),
    ]