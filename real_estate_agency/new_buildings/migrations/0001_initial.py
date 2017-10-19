# -*- coding: utf-8 -*-
# Generated by Django 1.10 on 2017-10-17 19:11
from __future__ import unicode_literals

from decimal import Decimal
from django.conf import settings
import django.core.validators
from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    initial = True

    dependencies = [
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
    ]

    operations = [
        migrations.CreateModel(
            name='Builder',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('name', models.CharField(max_length=127, unique=True, verbose_name='название фирмы застройщика')),
                ('web_site', models.URLField(blank=True, max_length=255, null=True, verbose_name='сайт застройщика')),
                ('logo', models.ImageField(upload_to='', verbose_name='логотип компании')),
                ('contact', models.ForeignKey(on_delete=django.db.models.deletion.PROTECT, to=settings.AUTH_USER_MODEL, verbose_name='контактное лицо')),
            ],
            options={
                'verbose_name_plural': 'застройщики',
                'verbose_name': 'застройщик',
            },
        ),
        migrations.CreateModel(
            name='NewApartment',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('total_area', models.DecimalField(decimal_places=2, max_digits=5, validators=[django.core.validators.MinValueValidator(Decimal('20.00'))], verbose_name='общая площадь (м2)')),
                ('description', models.TextField(verbose_name='описание')),
                ('celling_height', models.DecimalField(decimal_places=1, max_digits=2, validators=[django.core.validators.MinValueValidator(Decimal('2.0'))], verbose_name='высота потолка (м)')),
                ('interior_decoration', models.CharField(choices=[('D', 'ремонт'), ('ED', 'евро ремонт'), ('F', 'чистовая'), ('SF', 'предчистовая'), ('P', 'улучшенная черновая'), ('UF', 'черновая')], default='UF', max_length=31, verbose_name='вид отделки')),
                ('price', models.DecimalField(decimal_places=0, default=1000000, max_digits=15, validators=[django.core.validators.MinValueValidator(Decimal('0.0'))], verbose_name='цена, рб')),
                ('is_active', models.BooleanField(default=True, verbose_name='доступно на рынке')),
                ('date_added', models.DateTimeField(auto_now_add=True, verbose_name='добавлено')),
                ('last_modification', models.DateTimeField(auto_now=True, verbose_name='изменено')),
                ('apartment_number', models.IntegerField(verbose_name='Номер квартиры')),
                ('rooms', models.CharField(choices=[('B', 'студия'), ('1', '1'), ('2', '2'), ('3', '3'), ('4', '4'), ('5', '5'), ('6', '6'), ('7', '7')], default='1', help_text='Если вы не нашли нужного пункта - обратитесь к администратору', max_length=1, verbose_name='количество комнат')),
                ('kitchen_area', models.DecimalField(decimal_places=2, default=10, max_digits=5, validators=[django.core.validators.MinValueValidator(Decimal('10.00'))], verbose_name='площадь кухни (м2)')),
                ('floor', models.PositiveIntegerField(default=1, verbose_name='этаж')),
                ('section', models.PositiveIntegerField(default=1, validators=[django.core.validators.MinValueValidator(1)], verbose_name='подъезд/секция')),
                ('balcony_area', models.DecimalField(decimal_places=2, default=10, help_text='Если балкона нет - оставьте поле пустым', max_digits=5, validators=[django.core.validators.MinValueValidator(Decimal('10.00'))], verbose_name='площадь балкона (м2)')),
            ],
            options={
                'abstract': False,
                'verbose_name_plural': 'квартиры',
                'verbose_name': 'квартиры',
            },
        ),
        migrations.CreateModel(
            name='NewApartmentLayout',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('image', models.ImageField(upload_to='', verbose_name='изображения')),
                ('name', models.CharField(max_length=127, verbose_name='name')),
            ],
            options={
                'abstract': False,
                'verbose_name_plural': 'файлы',
                'verbose_name': 'файл',
            },
        ),
        migrations.CreateModel(
            name='NewBuilding',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('country', models.CharField(choices=[('RU', 'Россия')], default='RU', max_length=127, verbose_name='страна')),
                ('city', models.CharField(choices=[('RU-TMN', 'Тюмень')], default='RU-TMN', max_length=127, verbose_name='город')),
                ('neighbourhood', models.CharField(choices=[('MMS', 'ММС'), ('MYS', 'Мыс')], max_length=127, verbose_name='район')),
                ('street', models.CharField(max_length=127, verbose_name='улица')),
                ('building', models.IntegerField(verbose_name='дом')),
                ('building_block', models.IntegerField(blank=True, null=True, verbose_name='корпус')),
                ('zip_code', models.CharField(blank=True, max_length=127, null=True, verbose_name='почтовый индекс')),
                ('name', models.CharField(default='ГП', max_length=127, verbose_name='имя дома')),
                ('building_type', models.CharField(choices=[('BRICK', 'кирпичный'), ('MONO', 'монолитный'), ('FRAME', 'каркасный'), ('PANEL', 'панельный'), ('MFRAME', 'монолитно-каркасный'), ('BPANEL', 'панельный-кирпичный')], default='MONO', max_length=127, verbose_name='исполнение дома')),
                ('number_of_storeys', models.PositiveSmallIntegerField(validators=[django.core.validators.MinValueValidator(1)], verbose_name='количество этажей')),
                ('date_of_start_of_construction', models.DateField(blank=True, help_text='Важен только месяц', null=True, verbose_name='дата начала стройки')),
                ('date_of_construction', models.DateField(blank=True, help_text='Важен только месяц', null=True, verbose_name='дата постройки')),
                ('feed_link', models.URLField(blank=True, max_length=255, null=True, verbose_name='ссылка на фид')),
                ('active', models.BooleanField(default=True, verbose_name='отображать на сайте')),
            ],
            options={
                'abstract': False,
                'verbose_name_plural': 'дома',
                'verbose_name': 'дом',
            },
        ),
        migrations.CreateModel(
            name='ResidentalComplex',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('name', models.CharField(max_length=127, unique=True, verbose_name='название')),
                ('description', models.TextField(verbose_name='описание ЖК')),
                ('video_link', models.URLField(blank=True, null=True, verbose_name='ссылка на видео')),
                ('presentation', models.FileField(blank=True, null=True, upload_to='', verbose_name='презентация ЖК')),
                ('active', models.BooleanField(default=False, verbose_name='отображать в новостройках')),
                ('builder', models.ForeignKey(on_delete=django.db.models.deletion.PROTECT, to='new_buildings.Builder', verbose_name='застройщик')),
            ],
            options={
                'verbose_name_plural': 'жилые комплексы',
                'verbose_name': 'жилой комплекс',
            },
        ),
        migrations.CreateModel(
            name='ResidentalComplexСharacteristic',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
            ],
        ),
        migrations.AddField(
            model_name='residentalcomplex',
            name='characteristics',
            field=models.ManyToManyField(blank=True, to='new_buildings.ResidentalComplexСharacteristic', verbose_name='характеристики ЖК'),
        ),
        migrations.AddField(
            model_name='newbuilding',
            name='residental_complex',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='new_buildings.ResidentalComplex', verbose_name='ЖК'),
        ),
        migrations.AddField(
            model_name='newapartment',
            name='building',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='new_buildings.NewBuilding', verbose_name='строение'),
        ),
        migrations.AddField(
            model_name='newapartment',
            name='layout',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='new_buildings.NewApartmentLayout', verbose_name='планировка'),
        ),
        migrations.AddField(
            model_name='newapartment',
            name='posted_by',
            field=models.ForeignKey(default=None, editable=False, null=True, on_delete=django.db.models.deletion.SET_DEFAULT, to=settings.AUTH_USER_MODEL, verbose_name='разместил'),
        ),
        migrations.AlterUniqueTogether(
            name='newbuilding',
            unique_together=set([('street', 'building', 'building_block')]),
        ),
    ]
