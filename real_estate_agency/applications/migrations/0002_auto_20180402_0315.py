# -*- coding: utf-8 -*-
# Generated by Django 1.11 on 2018-04-01 22:15
from __future__ import unicode_literals

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('applications', '0001_initial'),
    ]

    operations = [
        migrations.AlterField(
            model_name='callbackrequest',
            name='extra_info',
            field=models.CharField(blank=True, max_length=1024, null=True, verbose_name='дополнительная информация'),
        ),
    ]