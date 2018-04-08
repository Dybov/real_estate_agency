# -*- coding: utf-8 -*-
# Generated by Django 1.10 on 2017-12-24 20:32
from __future__ import unicode_literals

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('new_buildings', '0004_auto_20171225_0015'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='newapartment',
            name='building',
        ),
        migrations.AddField(
            model_name='newapartment',
            name='buildings',
            field=models.ManyToManyField(to='new_buildings.NewBuilding', verbose_name='строения'),
        ),
        migrations.AddField(
            model_name='newapartment',
            name='residental_complex',
            field=models.ForeignKey(default=14, on_delete=django.db.models.deletion.CASCADE, to='new_buildings.ResidentalComplex', verbose_name='Комплекс'),
            preserve_default=False,
        ),
    ]