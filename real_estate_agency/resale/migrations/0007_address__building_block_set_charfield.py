# -*- coding: utf-8 -*-
# Generated by Django 1.11 on 2018-07-25 17:21
from __future__ import unicode_literals

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('resale', '0006_auto_20180718_2345'),
    ]

    operations = [
        migrations.AlterField(
            model_name='resaleapartment',
            name='building_block',
            field=models.CharField(blank=True, help_text='оставьте пустым, если поле не имеет смысла', max_length=5, null=True, verbose_name='корпус'),
        ),
    ]