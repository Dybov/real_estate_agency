# -*- coding: utf-8 -*-
# Generated by Django 1.10 on 2017-10-15 18:56
from __future__ import unicode_literals

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('new_buildings', '0001_initial'),
    ]

    operations = [
        migrations.AddField(
            model_name='building',
            name='name',
            field=models.CharField(default='ГП', max_length=127, verbose_name='имя дома'),
        ),
    ]
