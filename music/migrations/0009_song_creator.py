# -*- coding: utf-8 -*-
# Generated by Django 1.11.9 on 2018-02-22 13:28
from __future__ import unicode_literals

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('music', '0008_delete_myuser'),
    ]

    operations = [
        migrations.AddField(
            model_name='song',
            name='creator',
            field=models.CharField(default=0, max_length=200),
            preserve_default=False,
        ),
    ]