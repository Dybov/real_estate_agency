# -*- coding: utf-8 -*-
# Generated by Django 1.11 on 2018-03-17 22:31
from __future__ import unicode_literals

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('new_buildings', '0009_auto_20180302_0158'),
    ]

    operations = [
        migrations.AddField(
            model_name='residentalcomplex',
            name='number_of_buildings',
            field=models.PositiveIntegerField(blank=True, default=None, help_text='оставьте пустым для автоматического подсчета', null=True, verbose_name='количество домов в комплексе'),
        ),
    ]
