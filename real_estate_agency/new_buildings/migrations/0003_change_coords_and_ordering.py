# -*- coding: utf-8 -*-
# Generated by Django 1.11 on 2018-09-09 19:39
from __future__ import unicode_literals

import address.models
from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('new_buildings', '0002_builder_and_rcfeature_filepath'),
    ]

    operations = [
        migrations.AlterField(
            model_name='newbuilding',
            name='coordinates',
            field=address.models.CoordinateField(blank=True, max_length=127, null=True, verbose_name='широта,долгота'),
        ),
    ]
