# -*- coding: utf-8 -*-
# Generated by Django 1.11 on 2018-09-11 21:35
from __future__ import unicode_literals

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('resale', '0003_change_coords'),
    ]

    operations = [
        migrations.AlterModelOptions(
            name='resaleapartment',
            options={'ordering': ('-id',), 'permissions': (('can_add_change_delete_all_resale', 'Имеет доступ к чужим данным по вторичке'),), 'verbose_name': 'объект вторичка', 'verbose_name_plural': 'объекты вторички'},
        ),
    ]