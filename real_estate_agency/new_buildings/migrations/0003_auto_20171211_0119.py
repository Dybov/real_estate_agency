# -*- coding: utf-8 -*-
# Generated by Django 1.10 on 2017-12-10 20:19
from __future__ import unicode_literals

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('new_buildings', '0002_auto_20171207_2328'),
    ]

    operations = [
        migrations.AddField(
            model_name='residentalcomplex',
            name='is_popular',
            field=models.BooleanField(default=False, verbose_name='отображать на главной'),
        ),
        migrations.AlterField(
            model_name='residentalcomplex',
            name='is_active',
            field=models.BooleanField(default=False, verbose_name='отображать в новостройках'),
        ),
    ]
