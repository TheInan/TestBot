# -*- coding: utf-8 -*-
# Generated by Django 1.9.7 on 2016-06-08 17:22
from __future__ import unicode_literals

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('fb_firstbot', '0001_initial'),
    ]

    operations = [
        migrations.AddField(
            model_name='tracker',
            name='user_id',
            field=models.IntegerField(default=0),
        ),
    ]
