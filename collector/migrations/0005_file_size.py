# -*- coding: utf-8 -*-
# Generated by Django 1.11.7 on 2017-11-07 08:18
from __future__ import unicode_literals

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('collector', '0004_remove_file_size'),
    ]

    operations = [
        migrations.AddField(
            model_name='file',
            name='size',
            field=models.IntegerField(default=-1),
        ),
    ]