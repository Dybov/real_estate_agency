# -*- coding: utf-8 -*-
# Generated by Django 1.11 on 2018-10-28 17:57
from __future__ import unicode_literals

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('resale', '0006_resaleaparment_decoration'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='resaleapartment',
            name='interior_decoration',
        ),
    ]
