# -*- coding: utf-8 -*-
# Generated by Django 1.11 on 2018-07-15 13:29
from __future__ import unicode_literals

from django.db import migrations, models
import real_estate.models.helper


class Migration(migrations.Migration):

    dependencies = [
        ('company', '0001_initial'),
    ]

    operations = [
        migrations.CreateModel(
            name='BankPartner',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('image', models.ImageField(upload_to=real_estate.models.helper.get_file_path, verbose_name='изображение')),
                ('position', models.PositiveIntegerField(default=0, verbose_name='позиция')),
                ('title', models.CharField(max_length=127, verbose_name='название банка')),
            ],
            options={
                'verbose_name': 'объект банк-партнер',
                'verbose_name_plural': 'банки-партнеры',
                'ordering': ('position',),
            },
        ),
        migrations.AlterField(
            model_name='award',
            name='position',
            field=models.PositiveIntegerField(default=0, verbose_name='позиция'),
        ),
    ]
