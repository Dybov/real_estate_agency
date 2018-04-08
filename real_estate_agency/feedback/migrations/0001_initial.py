# -*- coding: utf-8 -*-
# Generated by Django 1.10 on 2017-12-24 21:31
from __future__ import unicode_literals

from django.db import migrations, models
import django.db.models.deletion
import real_estate.models


class Migration(migrations.Migration):

    initial = True

    dependencies = [
        ('new_buildings', '0006_auto_20171225_0231'),
    ]

    operations = [
        migrations.CreateModel(
            name='Feedback',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('author', models.CharField(max_length=127, verbose_name='клиент')),
                ('message', models.TextField(verbose_name='текст отзыва')),
                ('work_at', models.CharField(blank=True, max_length=127, null=True, verbose_name='место работы')),
                ('image', models.ImageField(upload_to=real_estate.models.get_file_path, verbose_name='фото')),
                ('is_active', models.BooleanField(default=True, verbose_name='отображать на сайте')),
                ('bought', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='new_buildings.ResidentalComplex')),
            ],
            options={
                'verbose_name': 'отзывы',
            },
        ),
    ]