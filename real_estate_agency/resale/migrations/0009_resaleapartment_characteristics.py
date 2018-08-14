# -*- coding: utf-8 -*-
# Generated by Django 1.11 on 2018-08-04 21:10
from __future__ import unicode_literals

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('real_estate', '0001_initial'),
        ('resale', '0008_auto_20180801_0043'),
    ]

    operations = [
        migrations.CreateModel(
            name='ResaleCharacteristic',
            fields=[
            ],
            options={
                'verbose_name_plural': 'характеристики вторички',
                'verbose_name': 'объект "характеристика вторички"',
                'proxy': True,
                'indexes': [],
            },
            bases=('real_estate.characteristic',),
        ),
        migrations.AddField(
            model_name='resaleapartment',
            name='characteristics',
            field=models.ManyToManyField(blank=True, to='real_estate.Characteristic', verbose_name='характеристики квартиры'),
        ),
    ]
