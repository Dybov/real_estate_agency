# -*- coding: utf-8 -*-
# Generated by Django 1.11 on 2018-05-19 20:54
from __future__ import unicode_literals

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('address', '0004_auto_20180226_0355'),
    ]

    operations = [
        migrations.AlterUniqueTogether(
            name='abstractaddressmodel',
            unique_together=set([]),
        ),
        migrations.RemoveField(
            model_name='abstractaddressmodel',
            name='neighbourhood',
        ),
        migrations.RemoveField(
            model_name='abstractaddressmodel',
            name='street',
        ),
        migrations.DeleteModel(
            name='AbstractAddressModel',
        ),
    ]
