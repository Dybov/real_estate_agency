import datetime
import re

from django.db import models
from django.db.models import Min, Max
from django.contrib.staticfiles.templatetags.staticfiles import static
from django.core.urlresolvers import reverse
from django.utils.translation import ugettext as _
from django.utils.functional import cached_property

from real_estate.models.apartment import Apartment
from real_estate.models.helper import get_file_path
from real_estate.models.image import (
    BasePropertyImage,
    spec_factory,
)
from real_estate.models.building import BaseBuildingWithoutNeighbourhood
from real_estate.models import Characteristic
from real_estate.templatetags.real_estate_extras import morphy_by_case
from address.models import NeighbourhoodModel

from .helpers import get_quarter_verbose
from real_estate.serializers import get_json_objects_with_props


new_buildings_spec_kwargs = {
    'width': 900,
    'height': 600,
    'format': 'JPEG',
    'options__quality': 75,
    'to_fit': False,
}


def get_quoted(_str):
    return "«" + _str + "»"


class NewApartment(Apartment):
    """ It will be objects of layouts for now """
    is_primary = True
    buildings = models.ManyToManyField('NewBuilding',
                                       verbose_name=_(
                                           'планировка присутсвует в домах'),
                                       )
    residental_complex = models.ForeignKey('ResidentalComplex',
                                           verbose_name=_('комплекс'),
                                           )
    date_of_construction = models.DateField(editable=False,
                                            null=True,
                                            blank=True,
                                            )
    layout_small = spec_factory(260, 250, source='layout')
    layout_large = spec_factory(690, 640, source='layout')

    def get_residental_complex(self):
        return self.residental_complex

    def get_neighbourhood(self):
        return self.residental_complex.neighbourhood

    def get_buildings(self):
        return self.buildings.filter(is_active=True)

    def get_date_of_construction(self):
        return get_quarter_verbose(self.date_of_construction)

    def _set_date_of_construction(self):
        """ Set self.date_of_construction
        as nearest date_of_construction of related buildings.

        return Bool changed this field or not"""
        buildings = self.get_buildings()

        date = buildings.aggregate(
            Min('date_of_construction')
        ).get('date_of_construction__min')
        date_origin = self.date_of_construction
        self.date_of_construction = date
        return not date_origin == date

    def is_built(self):
        if self.date_of_construction:
            return self.date_of_construction <= datetime.date.today()

    @property
    def full_price(self):
        return self.price

    class Meta:
        verbose_name = _('объект "планировка"')
        verbose_name_plural = _('планировки')
        ordering = ('rooms',)
    # Many to many fields "stocks" will appear in future


class BuildingWithRCMixin(models.Model):
    residental_complex = models.ForeignKey('ResidentalComplex',
                                           verbose_name=_('ЖК'),
                                           on_delete=models.CASCADE,
                                           )

    class Meta:
        abstract = True


class NewBuilding(BaseBuildingWithoutNeighbourhood, BuildingWithRCMixin):
    """it is building with concrete address,
    but it also has a name in ResidentalComlex area
    """
    name = models.CharField(verbose_name=_('имя дома'),
                            max_length=127,
                            default=_('ГП'),
                            )
    date_of_start_of_construction = models.DateField(
        verbose_name=_('дата начала стройки'),
        null=True,
        blank=True,
        help_text=_(
            'Важен только месяц'),
    )
    date_of_construction = models.DateField(
        verbose_name=_('дата окончания постройки'),
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
    building_permit = models.FileField(
        verbose_name=_('разрешение на строительство'),
        null=True,
        default=None,
        blank=True,
        upload_to=get_file_path,
    )
    project_declarations = models.FileField(
        verbose_name=_('проектная декларация'),
        null=True,
        default=None,
        blank=True,
        upload_to=get_file_path,
    )

    def get_apartments(self):
        return self.newapartment_set.filter(is_active=True)

    @property
    def get_quarter_of_construction(self):
        return get_quarter_verbose(self.date_of_construction)

    def __str__(self):
        return '%s' % (self.name, )

    class Meta(BaseBuildingWithoutNeighbourhood.Meta):
        unique_together = BaseBuildingWithoutNeighbourhood.Meta.\
            unique_together + (('name', 'residental_complex'), )

    def is_built(self):
        if self.date_of_construction:
            return self.date_of_construction <= datetime.date.today()
    is_built.short_description = _('Готовность дома')
    is_built.boolean = True


class TypeOfComplex(models.Model):
    """ it prefixes for ResidentalComplexes.
    Such as 'Жилой комплекс' or 'Микрорайон'.
    Which depends on builder policy in refer to concrete RC.
    """
    name = models.CharField(
        verbose_name=_('тип комплекса'),
        max_length=127,
        unique=True,
        help_text=_(
            'Необходимо писать в нижнем регистре. \
            Преобразование к верхнему регистру происходит автоматически'),
    )

    def __str__(self):
        return self.name.capitalize()

    def get_cased(self, case):
        return morphy_by_case(self.name, case)

    @cached_property
    def get_loct(self):
        return self.get_cased('loct')

    @cached_property
    def get_gent(self):
        return self.get_cased('gent')

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
                                            'Жилой комплекс/Микрорайон/...'),
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
    characteristics = models.ManyToManyField(
        'ResidentalComplexCharacteristic',
        verbose_name=_(
            'характеристики ЖК'),
        blank=True,
    )
    front_image = models.ImageField(verbose_name=_('основное изображение'),
                                    upload_to=get_file_path,
                                    blank=True, null=True,
                                    )
    front_image_spec_normal = spec_factory(
        source='front_image',
        **new_buildings_spec_kwargs
    )
    front_image_spec_heading = spec_factory(
        1200,
        900,
        source='front_image',
        format='JPEG',
        options__quality=100,
    )
    front_image_thumbnail = spec_factory(
        555,
        328,
        source='front_image',
        format='JPEG',
        to_fit=False,
        # options__quality=60,
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
    is_active = models.BooleanField(
        verbose_name=_('отображать в новостройках'),
        default=False,
    )
    is_popular = models.BooleanField(verbose_name=_('отображать на главной'),
                                     default=False,
                                     )
    number_of_flats = models.PositiveIntegerField(
        verbose_name=_('количество квартир в комплексе'),
        help_text=_(
            'оставьте пустым для автоматического подсчета'),
        default=None,
        null=True,
        blank=True,
    )
    number_of_buildings = models.PositiveIntegerField(
        verbose_name=_('количество домов в комплексе'),
        help_text=_(
            'оставьте пустым для автоматического подсчета'),
        default=None,
        null=True,
        blank=True,
    )

    neighbourhood = models.ForeignKey(NeighbourhoodModel,
                                      verbose_name=_('район'),
                                      on_delete=models.PROTECT,
                                      )
    date_of_construction = models.DateField(editable=False,
                                            null=True,
                                            blank=True,
                                            )
    lowest_price = models.DecimalField(editable=False,
                                       null=True,
                                       blank=True,
                                       decimal_places=0,
                                       max_digits=15,
                                       )

    def save(self, *args, **kwargs):
        # self._set_date_of_construction()
        super().save(*args, **kwargs)

    def get_date_of_construction(self):
        return get_quarter_verbose(self.date_of_construction)

    def _set_date_of_construction(self):
        buildings = self.get_new_buildings()

        date = buildings.aggregate(
            Max('date_of_construction')
        ).get('date_of_construction__max')
        date_original = self.date_of_construction
        self.date_of_construction = date
        return not date_original == date

    def get_features(self):
        return self.features.all()

    def get_characteristic(self):
        return self.characteristics.all()

    def get_new_apartments(self):
        return self.newapartment_set.filter(is_active=True,
                                            buildings__is_active=True,
                                            )

    def get_new_apartments_json(self):
        return get_json_objects_with_props(self.get_new_apartments())

    def get_new_buildings(self):
        return self.newbuilding_set.filter(is_active=True).prefetch_related(
            'newapartment_set')

    def get_new_buildings_json(self):
        return get_json_objects_with_props(
            self.get_new_buildings(),
            props=['get_quarter_of_construction']
        )

    def count_flats(self):
        if self.number_of_flats:
            return self.number_of_flats
        count = self.get_new_apartments().count()
        if count:
            return count
        return ""

    def count_buildings(self):
        if self.number_of_buildings:
            return self.number_of_buildings
        return len(self.get_new_buildings())

    @cached_property
    def min_and_max_dates(self):
        buildings = self.get_new_buildings()
        if buildings:
            return buildings.aggregate(
                min_date_of_construction=Min('date_of_construction'),
                max_date_of_construction=Max('date_of_construction'),
            )
        return {}

    def get_nearest_date_of_building(self, use_quarter=True):
        date = self.min_and_max_dates.get('min_date_of_construction', '')
        if use_quarter:
            return get_quarter_verbose(date)
        return date

    def get_latest_date_of_building(self, use_quarter=True):
        date = self.min_and_max_dates.get('max_date_of_construction', '')
        if use_quarter:
            return get_quarter_verbose(date)
        return date

    def get_title_photo_url(self):
        if self.front_image_spec_heading:
            return self.front_image_spec_heading.url
        return static('img/main.jpg')

    @cached_property
    def youtube_frame_link(self):
        if not self.video_link:
            return None

        link = re.sub(r'(.*youtube.com/)(watch\?v=)(.*)',
                      r'\1embed/\3',
                      self.video_link,
                      re.U | re.I,
                      )
        return link

    def min_and_max_prices(self):
        apartments = self.get_new_apartments()
        if apartments:
            return apartments.aggregate(
                min_price=Min('price'),
                max_price=Max('price'),
            )
        return {}

    def get_lowest_price(self):
        if self.lowest_price:
            return self.lowest_price
        return ''

    def get_highest_price(self):
        return self.min_and_max_prices().get('max_price')

    def _set_lowest_price(self):
        lowest_price_origin = self.lowest_price
        self.lowest_price = self.min_and_max_prices().get('min_price')

        return not self.lowest_price == lowest_price_origin

    def __str__(self):
        return self.get_quoted_name()

    def get_quoted_name(self):
        return get_quoted(self.name)

    def get_absolute_url(self):
        return reverse(
            'new_buildings:residental-complex-detail',
            args=[self.id]
        )

    def get_all_photos_url(self):
        urls = []
        if self.front_image:
            urls.append(self.front_image_spec_normal.url)
        for photo in self.photos.all():
            urls.append(photo.image_spec.url)
        return urls

    def is_built(self):
        if self.date_of_construction:
            return self.date_of_construction <= datetime.date.today()

    class Meta:
        verbose_name = _('комплекс')
        verbose_name_plural = _('комплексы')
        ordering = ('-is_popular',)


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
    logo = models.ImageField(verbose_name=_('логотип компании'),
                             blank=True,
                             null=True,
                             )

    def __str__(self):
        return self.get_quoted_name()

    def get_quoted_name(self):
        return get_quoted(self.name)

    class Meta:
        verbose_name = _('застройщик')
        verbose_name_plural = _('застройщики')


class ResidentalComplexCharacteristic(Characteristic):
    class Meta:
        verbose_name = _('характеристика комплекса')
        verbose_name_plural = _('характеристики комплексов')
        proxy = True


class ResidentalComplexFeature(models.Model):
    title = models.CharField(verbose_name=_('заголовок'),
                             max_length=127,
                             )
    description = models.TextField(verbose_name=_('описание'),
                                   max_length=500,
                                   )
    image = models.ImageField(verbose_name=_('изображение'))
    image_spec = spec_factory(680, 450, to_fit=False)
    residental_complex = models.ForeignKey(ResidentalComplex,
                                           on_delete=models.CASCADE,
                                           related_name='features',
                                           )

    def __str__(self):
        return self.title

    class Meta:
        verbose_name = _('особенность комплекса')
        verbose_name_plural = _('особенности комплекса')


class ResidentalComplexImage(BasePropertyImage):
    residental_complex = models.ForeignKey(ResidentalComplex,
                                           on_delete=models.CASCADE,
                                           related_name='photos',
                                           )
    image_spec = spec_factory(
        **new_buildings_spec_kwargs
    )
