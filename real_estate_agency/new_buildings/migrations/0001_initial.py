# -*- coding: utf-8 -*-
# Generated by Django 1.11 on 2018-08-19 19:46
from __future__ import unicode_literals

from decimal import Decimal
from django.conf import settings
import django.core.validators
from django.db import migrations, models
import django.db.models.deletion
import real_estate.models.helper


class Migration(migrations.Migration):

    initial = True

    dependencies = [
        ('address', '0001_initial'),
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
        ('real_estate', '0001_initial'),
    ]

    operations = [
        migrations.CreateModel(
            name='Builder',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('name', models.CharField(max_length=127, unique=True, verbose_name='название фирмы застройщика')),
                ('web_site', models.URLField(blank=True, max_length=255, null=True, verbose_name='сайт застройщика')),
                ('logo', models.ImageField(blank=True, null=True, upload_to='', verbose_name='логотип компании')),
            ],
            options={
                'verbose_name': 'застройщик',
                'verbose_name_plural': 'застройщики',
            },
        ),
        migrations.CreateModel(
            name='NewApartment',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('layout', models.ImageField(upload_to=real_estate.models.helper.get_file_path, verbose_name='планировка')),
                ('total_area', models.DecimalField(decimal_places=2, max_digits=5, validators=[django.core.validators.MinValueValidator(Decimal('15.00'))], verbose_name='общая площадь (м2)')),
                ('interior_decoration', models.CharField(choices=[('D', 'ремонт'), ('ED', 'евро ремонт'), ('F', 'чистовая'), ('SF', 'предчистовая'), ('P', 'улучшенная черновая'), ('UF', 'черновая')], default='UF', max_length=31, verbose_name='вид отделки')),
                ('price', models.DecimalField(decimal_places=0, default=1000000, max_digits=15, validators=[django.core.validators.MinValueValidator(Decimal('0.0'))], verbose_name='цена, рб')),
                ('description', models.TextField(blank=True, null=True, verbose_name='описание')),
                ('celling_height', models.DecimalField(decimal_places=1, default=2.7, max_digits=2, validators=[django.core.validators.MinValueValidator(Decimal('2.0'))], verbose_name='высота потолка (м)')),
                ('is_active', models.BooleanField(default=True, verbose_name='отображать на сайте')),
                ('date_added', models.DateTimeField(auto_now_add=True, verbose_name='добавлено')),
                ('last_modification', models.DateTimeField(auto_now=True, verbose_name='изменено')),
                ('rooms', models.CharField(choices=[('B', 'студия'), ('1', '1'), ('2', '2'), ('3', '3'), ('4', '4'), ('5', '5'), ('6', '6'), ('7', '7')], default='1', help_text='Если вы не нашли нужного пункта - обратитесь к администратору', max_length=1, verbose_name='количество комнат')),
                ('floor', models.CharField(default=1, max_length=127, verbose_name='этаж')),
                ('section', models.PositiveIntegerField(default=1, validators=[django.core.validators.MinValueValidator(1)], verbose_name='подъезд/секция')),
                ('kitchen_area', models.DecimalField(decimal_places=2, default=5, max_digits=5, validators=[django.core.validators.MinValueValidator(Decimal('5.00'))], verbose_name='площадь кухни (м2)')),
                ('balcony_area', models.DecimalField(blank=True, decimal_places=2, default=0, max_digits=5, null=True, validators=[django.core.validators.MinValueValidator(Decimal('0.00'))], verbose_name='площадь балкона (м2)')),
                ('date_of_construction', models.DateField(blank=True, editable=False, null=True)),
            ],
            options={
                'verbose_name': 'объект "планировка"',
                'verbose_name_plural': 'планировки',
                'ordering': ('rooms',),
            },
        ),
        migrations.CreateModel(
            name='NewBuilding',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('building', models.IntegerField(validators=[django.core.validators.MinValueValidator(1)], verbose_name='номер дома')),
                ('building_block', models.CharField(blank=True, help_text='оставьте пустым, если поле не имеет смысла', max_length=5, null=True, verbose_name='корпус')),
                ('zip_code', models.CharField(blank=True, max_length=127, null=True, verbose_name='почтовый индекс')),
                ('coordinates', models.CharField(blank=True, max_length=127, null=True, verbose_name='широта,долгота')),
                ('building_type', models.CharField(choices=[('BRICK', 'кирпичный'), ('MONO', 'монолитный'), ('FRAME', 'каркасный'), ('PANEL', 'панельный'), ('MFRAME', 'монолитно-каркасный'), ('BPANEL', 'панельный-кирпичный'), ('RCBLOCK', 'блоки железобетоные'), ('SBLOCK', 'cиликатный блок')], default='MONO', max_length=127, verbose_name='исполнение дома')),
                ('number_of_storeys', models.PositiveSmallIntegerField(default=1, validators=[django.core.validators.MinValueValidator(1)], verbose_name='количество этажей')),
                ('name', models.CharField(default='ГП', max_length=127, verbose_name='имя дома')),
                ('date_of_start_of_construction', models.DateField(blank=True, help_text='Важен только месяц', null=True, verbose_name='дата начала стройки')),
                ('date_of_construction', models.DateField(blank=True, help_text='Важен только месяц', null=True, verbose_name='дата окончания постройки')),
                ('feed_link', models.URLField(blank=True, max_length=255, null=True, verbose_name='ссылка на фид')),
                ('is_active', models.BooleanField(default=True, verbose_name='отображать на сайте')),
                ('building_permit', models.FileField(blank=True, default=None, null=True, upload_to=real_estate.models.helper.get_file_path, verbose_name='разрешение на строительство')),
                ('project_declarations', models.FileField(blank=True, default=None, null=True, upload_to=real_estate.models.helper.get_file_path, verbose_name='проектная декларация')),
            ],
            options={
                'verbose_name': 'дом',
                'verbose_name_plural': 'дома',
                'abstract': False,
            },
        ),
        migrations.CreateModel(
            name='ResidentalComplex',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('name', models.CharField(max_length=127, unique=True, verbose_name='название')),
                ('description', models.TextField(verbose_name='описание ЖК')),
                ('front_image', models.ImageField(blank=True, null=True, upload_to=real_estate.models.helper.get_file_path, verbose_name='основное изображение')),
                ('video_link', models.URLField(blank=True, null=True, verbose_name='ссылка на видео')),
                ('presentation', models.FileField(blank=True, null=True, upload_to='', verbose_name='презентация ЖК')),
                ('is_active', models.BooleanField(default=False, verbose_name='отображать в новостройках')),
                ('is_popular', models.BooleanField(default=False, verbose_name='отображать на главной')),
                ('number_of_flats', models.PositiveIntegerField(blank=True, default=None, help_text='оставьте пустым для автоматического подсчета', null=True, verbose_name='количество квартир в комплексе')),
                ('number_of_buildings', models.PositiveIntegerField(blank=True, default=None, help_text='оставьте пустым для автоматического подсчета', null=True, verbose_name='количество домов в комплексе')),
                ('date_of_construction', models.DateField(blank=True, editable=False, null=True)),
                ('lowest_price', models.DecimalField(blank=True, decimal_places=0, editable=False, max_digits=15, null=True)),
                ('builder', models.ForeignKey(on_delete=django.db.models.deletion.PROTECT, to='new_buildings.Builder', verbose_name='застройщик')),
            ],
            options={
                'verbose_name': 'комплекс',
                'verbose_name_plural': 'комплексы',
                'ordering': ('-is_popular',),
            },
        ),
        migrations.CreateModel(
            name='ResidentalComplexFeature',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('title', models.CharField(max_length=127, verbose_name='заголовок')),
                ('description', models.TextField(max_length=500, verbose_name='описание')),
                ('image', models.ImageField(upload_to='', verbose_name='изображение')),
                ('residental_complex', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='features', to='new_buildings.ResidentalComplex')),
            ],
            options={
                'verbose_name': 'особенность комплекса',
                'verbose_name_plural': 'особенности комплекса',
            },
        ),
        migrations.CreateModel(
            name='ResidentalComplexImage',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('image', models.ImageField(upload_to=real_estate.models.helper.get_file_path, verbose_name='изображение')),
                ('residental_complex', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='photos', to='new_buildings.ResidentalComplex')),
            ],
            options={
                'verbose_name': 'изображение',
                'verbose_name_plural': 'изображения',
                'abstract': False,
            },
        ),
        migrations.CreateModel(
            name='TypeOfComplex',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('name', models.CharField(help_text='Необходимо писать в нижнем регистре.             Преобразование к верхнему регистру происходит автоматически', max_length=127, unique=True, verbose_name='тип комплекса')),
            ],
            options={
                'verbose_name': 'тип комплекса',
                'verbose_name_plural': 'типы комплексов',
            },
        ),
        migrations.CreateModel(
            name='ResidentalComplexCharacteristic',
            fields=[
            ],
            options={
                'verbose_name': 'характеристика комплекса',
                'verbose_name_plural': 'характеристики комплексов',
                'indexes': [],
                'proxy': True,
            },
            bases=('real_estate.characteristic',),
        ),
        migrations.AddField(
            model_name='residentalcomplex',
            name='characteristics',
            field=models.ManyToManyField(blank=True, to='new_buildings.ResidentalComplexCharacteristic', verbose_name='характеристики ЖК'),
        ),
        migrations.AddField(
            model_name='residentalcomplex',
            name='neighbourhood',
            field=models.ForeignKey(on_delete=django.db.models.deletion.PROTECT, to='address.NeighbourhoodModel', verbose_name='район'),
        ),
        migrations.AddField(
            model_name='residentalcomplex',
            name='type_of_complex',
            field=models.ForeignKey(default=1, help_text='Жилой комплекс/Микрорайон/...', on_delete=django.db.models.deletion.PROTECT, to='new_buildings.TypeOfComplex', verbose_name='тип комплекса'),
        ),
        migrations.AddField(
            model_name='newbuilding',
            name='residental_complex',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='new_buildings.ResidentalComplex', verbose_name='ЖК'),
        ),
        migrations.AddField(
            model_name='newbuilding',
            name='street',
            field=models.ForeignKey(on_delete=django.db.models.deletion.PROTECT, to='address.StreetModel', verbose_name='улица'),
        ),
        migrations.AddField(
            model_name='newapartment',
            name='buildings',
            field=models.ManyToManyField(to='new_buildings.NewBuilding', verbose_name='планировка присутсвует в домах'),
        ),
        migrations.AddField(
            model_name='newapartment',
            name='created_by',
            field=models.ForeignKey(default=None, null=True, on_delete=django.db.models.deletion.SET_DEFAULT, related_name='new_buildings_newapartment_created', to=settings.AUTH_USER_MODEL, verbose_name='создано'),
        ),
        migrations.AddField(
            model_name='newapartment',
            name='modified_by',
            field=models.ForeignKey(default=None, null=True, on_delete=django.db.models.deletion.SET_DEFAULT, related_name='new_buildings_newapartment_modified', to=settings.AUTH_USER_MODEL, verbose_name='изменено'),
        ),
        migrations.AddField(
            model_name='newapartment',
            name='residental_complex',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='new_buildings.ResidentalComplex', verbose_name='комплекс'),
        ),
        migrations.AlterUniqueTogether(
            name='newbuilding',
            unique_together=set([('name', 'residental_complex'), ('street', 'building', 'building_block')]),
        ),
    ]
