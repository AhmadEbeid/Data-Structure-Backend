# -*- coding: utf-8 -*-
# Generated by Django 1.11.7 on 2018-04-26 15:21
from __future__ import unicode_literals

from django.conf import settings
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('socialNetwork', '0003_auto_20180426_1718'),
    ]

    operations = [
        migrations.AlterField(
            model_name='postsmodel',
            name='likes',
            field=models.ManyToManyField(blank=True, to=settings.AUTH_USER_MODEL),
        ),
    ]
