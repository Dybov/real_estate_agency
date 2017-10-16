# -*- coding: utf-8 -*-
# Generated by Django 1.10 on 2017-10-16 18:11
from __future__ import unicode_literals

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('new_buildings', '0004_auto_20171016_2306'),
    ]

    operations = [
        migrations.AddField(
            model_name='newbuilding',
            name='date_of_start_of_construction',
            field=models.DateField(blank=True, help_text='Важно указать только месяц', null=True, verbose_name='дата начала стройки'),
        ),
        migrations.AlterField(
            model_name='residentalcomplex',
            name='characteristics',
            field=models.ManyToManyField(blank=True, null=True, to='new_buildings.ResidentalComplexСharacteristic', verbose_name='характеристики ЖК'),
        ),
    ]
