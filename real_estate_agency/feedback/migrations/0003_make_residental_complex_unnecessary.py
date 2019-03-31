# -*- coding: utf-8 -*-
# Generated by Django 1.11 on 2019-02-19 20:26
from __future__ import unicode_literals

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('feedback', '0002_add_is_resale_field'),
    ]

    operations = [
        migrations.AlterField(
            model_name='feedback',
            name='residental_complex',
            field=models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.CASCADE, to='new_buildings.ResidentalComplex', verbose_name='ЖК'),
        ),
    ]
