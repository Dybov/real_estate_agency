# -*- coding: utf-8 -*-
# Generated by Django 1.11 on 2018-10-22 18:44
from __future__ import unicode_literals

from django.db import migrations, models
import django.db.models.deletion

import real_estate

from real_estate.models.property import BasePropertyModel


def fill_decoration_based_on_prev_field(apps, schema_editor):
    """ It resaves data from interior_decoration field to FK decoration"""
    Apartment = apps.get_model("resale", "resaleapartment")
    Decoration = apps.get_model("real_estate", "decoration")

    choices = dict(BasePropertyModel.INTERIOR_DECORATION_CHOICES)
    for abbr, name in choices.items():
        obj = Decoration.objects.get(name=name)
        choices[abbr] = obj

    for apartment in Apartment.objects.all():
        decoration = apartment.interior_decoration
        new_decoration = choices.get(decoration)
        apartment.decoration = new_decoration
        apartment.save()


class Migration(migrations.Migration):

    dependencies = [
        ('real_estate', '0002_decoration'),
        ('resale', '0005_draggable_images'),
    ]

    operations = [
        migrations.AlterField(
            model_name='resaleapartment',
            name='layout',
            field=models.ImageField(blank=True, upload_to=real_estate.models.helper.get_file_path, verbose_name='планировка'),
        ),
        migrations.AddField(
            model_name='resaleapartment',
            name='decoration',
            field=models.ForeignKey(null=True, on_delete=django.db.models.deletion.CASCADE, to='real_estate.Decoration', verbose_name='вид отделки'),
        ),
        migrations.RunPython(
            fill_decoration_based_on_prev_field,
            reverse_code=migrations.RunPython.noop
        ),
        migrations.CreateModel(
            name='ResaleDecoration',
            fields=[
            ],
            options={
                'indexes': [],
                'proxy': True,
                'verbose_name': 'тип отделки/ремонта',
                'verbose_name_plural': 'типы отделки/ремонта',
            },
            bases=('real_estate.decoration',),
        ),
    ]
