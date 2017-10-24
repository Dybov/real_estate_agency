import datetime

from django.db import models
from django.contrib.auth.models import User
from django.core.validators import MinValueValidator
from django.utils.translation import ugettext as _

from real_estate.models import Apartment, get_file_path, BasePropertyImage
from address.models import Address


class NewApartment(Apartment):
    """ It will be objects of layouts for now """
    is_primary = True
    building = models.ForeignKey('NewBuilding',
                                 verbose_name=_('строение'),
                                 on_delete=models.CASCADE,
                                 )
    # Many to many fields "stocks" will appear in future


class NewBuilding(Address):
    """it is building with concrete address,
    but it also has a name in ResidentalComlex area
    """
    TYPE_BRICK = 'BRICK'
    TYPE_MONOLITHIC = 'MONO'
    TYPE_FRAME = 'FRAME'
    TYPE_PANEL = 'PANEL'
    TYPE_MONOLITHIC_FRAME = 'MFRAME'
    TYPE_BRICK_PANEL = 'BPANEL'
    BUILDING_TYPE_CHOICES = (
        (TYPE_BRICK, _('кирпичный')),
        (TYPE_MONOLITHIC, _('монолитный')),
        (TYPE_FRAME, _('каркасный')),
        (TYPE_PANEL, _('панельный')),
        (TYPE_MONOLITHIC_FRAME, _('монолитно-каркасный')),
        (TYPE_BRICK_PANEL, _('панельный-кирпичный')),
    )

    name = models.CharField(verbose_name=_('имя дома'),
                            max_length=127,
                            default=_('ГП'),
                            )
    residental_complex = models.ForeignKey('ResidentalComplex',
                                           verbose_name=_('ЖК'),
                                           on_delete=models.CASCADE,
                                           )
    building_type = models.CharField(max_length=127,
                                     verbose_name=_('исполнение дома'),
                                     choices=BUILDING_TYPE_CHOICES,
                                     default=TYPE_MONOLITHIC,
                                     )
    number_of_storeys = models.PositiveSmallIntegerField(
        verbose_name=_('количество этажей'),
        validators=[MinValueValidator(1)],
    )
    date_of_start_of_construction = models.DateField(verbose_name=_('дата начала стройки'),
                                                     null=True,
                                                     blank=True,
                                                     help_text=_(
        'Важен только месяц'),
    )
    date_of_construction = models.DateField(verbose_name=_('дата окончания постройки'),
                                            null=True,
                                            blank=True,
                                            help_text=_(
                                                'Важен только месяц'),
                                            )
    feed_link = models.URLField(verbose_name=_('ссылка на фид'),
                                max_length=255,
                                null=True,
                                blank=True,
                                )
    is_active = models.BooleanField(verbose_name=_('отображать на сайте'),
                                    default=True,
                                    )

    def get_apartments(self):
        return self.newapartment_set.filter(is_active=True)

    def __str__(self):
        return '%s' % (self.name, )

    class Meta(Address.Meta):
        verbose_name = _('дом')
        verbose_name_plural = _('дома')
        unique_together = Address.Meta.unique_together + \
            (('name', 'residental_complex'), )

    def is_built(self):
        if self.date_of_construction:
            return self.date_of_construction <= datetime.date.today()
    is_built.short_description = _('Готовность дома')
    is_built.boolean = True


class TypeOfComplex(models.Model):
    """ it prefixes for ResidentalComplexes.
    Such as 'Жилой комплекс' or 'Микрорайон', which depends on builder policy
    """
    name = models.CharField(verbose_name=_('тип комплекса'),
                            max_length=127,
                            unique=True,
                            help_text=_(
                                'Необходимо писать в нижнем регистре. Преобразование к верхнему регистру происходит автоматически'),
                            )

    def __str__(self):
        return self.name

    class Meta:
        verbose_name = _('тип комплекса')
        verbose_name_plural = _('типы комплексов')


class ResidentalComplex(models.Model):
    """ it is aggregate of houses.
    They are built in the same style by the same builder.
    """
    type_of_complex = models.ForeignKey(TypeOfComplex,
                                        verbose_name=_('тип комплекса'),
                                        default=1,
                                        help_text=_(
                                            'Жилой комплекс/Мирорайон/...'),
                                        on_delete=models.PROTECT,
                                        )

    name = models.CharField(verbose_name=_('название'),
                            max_length=127,
                            unique=True,
                            )
    description = models.TextField(verbose_name=_('описание ЖК'),)
    builder = models.ForeignKey('Builder',
                                verbose_name=_('застройщик'),
                                on_delete=models.PROTECT,
                                )
    # one to many "photos"
    characteristics = models.ManyToManyField('ResidentalComplexСharacteristic',
                                             verbose_name=_(
                                                 'характеристики ЖК'),
                                             blank=True,)
    front_image = models.ImageField(verbose_name=_('Основное изображение'),
                                    upload_to=get_file_path,
                                    )
    # one to many "features"
    # one to many "houses"
    video_link = models.URLField(verbose_name=_('ссылка на видео'),
                                 null=True,
                                 blank=True,
                                 )
    presentation = models.FileField(verbose_name=_('презентация ЖК'),
                                    null=True,
                                    blank=True,
                                    )
    # one to many "documents_for_construction"
    is_active = models.BooleanField(verbose_name=_('отображать на сайте'),
                                    default=False,
                                    )
    def get_features(self):
        return self.features.all()

    def building_type(self):
        buildings = self.get_new_buildings()
        if buildings:
            return buildings[0].get_building_type_display()
        return '-'

    def get_new_buildings(self):
        return self.newbuilding_set.filter(is_active=True)

    def count_flats(self):
        count = 0
        for building in self.get_new_buildings():
            count += len(building.get_apartments())
        return count

    def count_buildings(self):
        return len(self.get_new_buildings())

    def get_nearest_date_of_building(self):
        from django.db.models import Min
        buildings = self.newbuilding_set.all()
        if buildings:
            return buildings.annotate(Min('date_of_construction'))[0].date_of_construction

    def get_latest_date_of_building(self):
        from django.db.models import Max
        buildings = self.newbuilding_set.all()
        if buildings:
            return buildings.annotate(Max('date_of_construction'))[0].date_of_construction

    def get_title_photo_url(self):
        if self.photos.all():
            return self.front_image.url

    def __str__(self):
        return self.name

    class Meta:
        verbose_name = _('комплекс')
        verbose_name_plural = _('комплексы')


class Builder(models.Model):
    name = models.CharField(max_length=127,
                            unique=True,
                            verbose_name=_('название фирмы застройщика'),
                            )
    web_site = models.URLField(verbose_name=_('сайт застройщика'),
                               max_length=255,
                               null=True,
                               blank=True,
                               )
    contact = models.ForeignKey(User,
                                on_delete=models.PROTECT,
                                verbose_name=_('контактное лицо'),
                                )
    logo = models.ImageField(verbose_name=_('логотип компании'))

    def __str__(self):
        return self.name

    class Meta:
        verbose_name = _('застройщик')
        verbose_name_plural = _('застройщики')


class ResidentalComplexСharacteristic(models.Model):
    characteristic = models.CharField(verbose_name=_('характеристика'),
                                      max_length=127,
                                      unique=True,
                                      )
    icon = models.ImageField(verbose_name=_('иконка'))

    def __str__(self):
        return self.characteristic

    class Meta:
        verbose_name=_('характеристика')
        verbose_name_plural = _('характеристики')

class ResidentalComplexFeature(models.Model):
    title = models.CharField(verbose_name=_('заголовок'),
                             max_length=127,
                             )
    description = models.TextField(verbose_name=_('описание'),
                                   max_length=500,
                                   )
    image = models.ImageField(verbose_name=_('изображение'))
    residental_complex = models.ForeignKey(ResidentalComplex,
                                           on_delete=models.CASCADE,
                                           related_name='features',
                                           )
    def __str__(self):
        return self.title

    class Meta:
        verbose_name=_('особенность комплекса')
        verbose_name_plural = _('особенности комплекса')


class ResidentalComplexImage(BasePropertyImage):
    residental_complex = models.ForeignKey(ResidentalComplex,
                                           on_delete=models.CASCADE,
                                           related_name='photos',
                                           )
