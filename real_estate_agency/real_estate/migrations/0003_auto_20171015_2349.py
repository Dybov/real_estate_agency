# -*- coding: utf-8 -*-
# Generated by Django 1.10 on 2017-10-15 18:49
from __future__ import unicode_literals

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('real_estate', '0002_auto_20171015_2236'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='apartment',
            name='posted_by',
        ),
        migrations.DeleteModel(
            name='Apartment',
        ),
    ]
