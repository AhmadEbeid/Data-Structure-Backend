# -*- coding: utf-8 -*-
# Generated by Django 1.11.7 on 2018-05-15 13:16
from __future__ import unicode_literals

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('socialNetwork', '0006_auto_20180505_0211'),
    ]

    operations = [
        migrations.AddField(
            model_name='profilemodel',
            name='image',
            field=models.FileField(blank=True, upload_to='media/images/'),
        ),
    ]