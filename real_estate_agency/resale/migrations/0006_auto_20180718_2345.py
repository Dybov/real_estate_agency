# -*- coding: utf-8 -*-
# Generated by Django 1.11 on 2018-07-18 18:45
from __future__ import unicode_literals

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('resale', '0005_auto_20180618_0010'),
    ]

    operations = [
        migrations.AlterField(
            model_name='resaleapartment',
            name='related_mortgage',
            field=models.ForeignKey(blank=True, default=None, help_text='если находится в ипотеке', null=True, on_delete=django.db.models.deletion.CASCADE, to='company.BankPartner', verbose_name='В ипотеке у'),
        ),
    ]
