# -*- coding: utf-8 -*-
# Generated by Django 1.11 on 2018-02-17 20:48
from __future__ import unicode_literals

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('address', '0002_abstractaddressmodel_coordinates'),
    ]

    operations = [
        migrations.AlterField(
            model_name='abstractaddressmodel',
            name='coordinates',
            field=models.CharField(blank=True, max_length=127, null=True, verbose_name='широта,долгота'),
        ),
    ]
