import datetime

from django.db import models
from django.contrib.auth.models import User
from django.contrib.staticfiles.templatetags.staticfiles import static
from django.core.validators import MinValueValidator
from django.utils.translation import ugettext as _
from django.utils.functional import cached_property

from .helpers import get_quarter


from real_estate.models import Apartment, get_file_path, BasePropertyImage
from address.models import AbstractAddressModelWithoutNeighbourhood, NeighbourhoodModel


def get_json_object(_object, props=[]):
    from django.core.serializers import serialize
    from .serializers import ExtJsonSerializer
    from django.utils.safestring import mark_safe
    return mark_safe(ExtJsonSerializer().serialize(_object, props=props))


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

    def get_residental_complex(self):
        return self.residental_complex

    def get_neighbourhood(self):
        return self.residental_complex.neighbourhood

    def get_buildings(self):
        return self.buildings.filter(is_active=True)

    class Meta:
        verbose_name = _('объект "планировка"')
        verbose_name_plural = _('планировки')
    # Many to many fields "stocks" will appear in future


class NewBuilding(AbstractAddressModelWithoutNeighbourhood):
    """it is building with concrete address,
    but it also has a name in ResidentalComlex area
    """
    # Type of building material
    TYPE_BRICK = 'BRICK'
    TYPE_MONOLITHIC = 'MONO'
    TYPE_FRAME = 'FRAME'
    TYPE_PANEL = 'PANEL'
    TYPE_MONOLITHIC_FRAME = 'MFRAME'
    TYPE_BRICK_PANEL = 'BPANEL'
    TYPE_REINFORCED_CONCRETE_BLOCKS = 'RCBLOCK'
    TYPE_SILICAT_BLOCK = "SBLOCK"
    BUILDING_TYPE_CHOICES = (
        (TYPE_BRICK, _('кирпичный')),
        (TYPE_MONOLITHIC, _('монолитный')),
        (TYPE_FRAME, _('каркасный')),
        (TYPE_PANEL, _('панельный')),
        (TYPE_MONOLITHIC_FRAME, _('монолитно-каркасный')),
        (TYPE_BRICK_PANEL, _('панельный-кирпичный')),
        (TYPE_REINFORCED_CONCRETE_BLOCKS, _('блоки железобетоные')),
        (TYPE_SILICAT_BLOCK, _('cиликатный блок')),
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
    building_permit = models.FileField(verbose_name=_('разрешение на строительство'),
                                       null=True,
                                       default=None,
                                       blank=True,
                                       upload_to=get_file_path,
                                       )
    project_declarations = models.FileField(verbose_name=_('проектная декларация'),
                                            null=True,
                                            default=None,
                                            blank=True,
                                            upload_to=get_file_path,
                                            )

    def get_apartments(self):
        return self.newapartment_set.filter(is_active=True)

    @property
    def get_quarter_of_construction(self):
        if self.date_of_construction:
            return get_quarter(self.date_of_construction)['verbose_name']
        else:
            return ''

    def __str__(self):
        return '%s' % (self.name, )

    class Meta(AbstractAddressModelWithoutNeighbourhood.Meta):
        verbose_name = _('дом')
        verbose_name_plural = _('дома')
        unique_together = AbstractAddressModelWithoutNeighbourhood.Meta.unique_together + \
            (('name', 'residental_complex'), )

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
    name = models.CharField(verbose_name=_('тип комплекса'),
                            max_length=127,
                            unique=True,
                            help_text=_(
                                'Необходимо писать в нижнем регистре. Преобразование к верхнему регистру происходит автоматически'),
                            )

    def __str__(self):
        return self.name.capitalize()

    def get_cased(self, case):
        from real_estate.templatetags.real_estate_extras import morphy_by_case
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
    characteristics = models.ManyToManyField('ResidentalComplexСharacteristic',
                                             verbose_name=_(
                                                 'характеристики ЖК'),
                                             blank=True,)
    front_image = models.ImageField(verbose_name=_('основное изображение'),
                                    upload_to=get_file_path,
                                    blank=True, null=True,
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
    is_active = models.BooleanField(verbose_name=_('отображать в новостройках'),
                                    default=False,
                                    )
    is_popular = models.BooleanField(verbose_name=_('отображать на главной'),
                                     default=False,
                                     )
    number_of_flats = models.PositiveIntegerField(verbose_name=_('количество квартир в комплексе'),
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

    def get_features(self):
        return self.features.all()

    def get_characteristic(self):
        return self.characteristics.all()

    @cached_property
    def get_new_apartments(self):
        return self.newapartment_set.filter(is_active=True)

    def get_new_apartments_json(self):
        return get_json_object(self.get_new_apartments)

    @cached_property
    def get_new_buildings(self):
        return self.newbuilding_set.filter(is_active=True).prefetch_related('newapartment_set')

    def get_new_buildings_json(self):
        return get_json_object(self.get_new_buildings, props=['get_quarter_of_construction'])

    def count_flats(self):
        if self.number_of_flats:
            return self.number_of_flats
        count = 0
        for building in self.get_new_buildings:
            count += len(building.get_apartments())
        return count

    def count_buildings(self):
        return len(self.get_new_buildings)

    @cached_property
    def min_and_max_dates(self):
        from django.db.models import Min, Max

        buildings = self.get_new_buildings
        if buildings:
            return buildings.aggregate(
                min_date_of_construction=Min('date_of_construction'),
                max_date_of_construction=Max('date_of_construction'),
            )
        return {}

    def get_nearest_date_of_building(self, use_quarter=True):
        date=self.min_and_max_dates.get('min_date_of_construction')
        if not date:
            return ''
        if use_quarter:
            qrtr = get_quarter(date)   
            return qrtr['verbose_name']
        return date

    def get_latest_date_of_building(self, use_quarter=True):
        date=self.min_and_max_dates.get('max_date_of_construction')
        if not date:
            return ''
        if use_quarter:
            qrtr = get_quarter(date)
            return qrtr['verbose_name']
        return date

    def get_title_photo_url(self):
        if self.front_image:
            return self.front_image.url
        return static('img/main.jpg') 

    @cached_property
    def youtube_frame_link(self):
        if not self.video_link:
            return None

        import re
        link = re.sub(r'(.*youtube.com/)(watch\?v=)(.*)',
                      r'\1embed/\3',
                      self.video_link,
                      re.U | re.I,
                      )
        return link

    @cached_property
    def min_and_max_prices(self):
        from django.db.models import Min, Max

        # For union all combines querysets
        apartments = None

        buildings = self.get_new_buildings
        if buildings:
            for building in buildings:
                if not apartments:
                    apartments = building.get_apartments()
                else:
                    apartments.union(building.get_apartments())
            if apartments:
                return apartments.aggregate(
                    min_price=Min('price'),
                    max_price=Max('price'),
                )
        return {}

    def get_lowest_price(self):
        return self.min_and_max_prices.get('min_price')

    def get_highest_price(self):
        return self.min_and_max_prices.get('max_price')

    def __str__(self):
        return self.name

    def get_absolute_url(self):
        from django.core.urlresolvers import reverse
        return reverse('new_buildings:residental-complex-detail', args=[self.id])

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
    logo = models.ImageField(verbose_name=_('логотип компании'),
                             blank=True,
                             null=True,
                             )

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
    icon = models.ImageField(verbose_name=_('иконка'),
                             upload_to=get_file_path,
                             )

    def __str__(self):
        return self.characteristic

    class Meta:
        verbose_name = _('характеристика комплекса')
        verbose_name_plural = _('характеристики комплексов')


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
        verbose_name = _('особенность комплекса')
        verbose_name_plural = _('особенности комплекса')


class ResidentalComplexImage(BasePropertyImage):
    residental_complex = models.ForeignKey(ResidentalComplex,
                                           on_delete=models.CASCADE,
                                           related_name='photos',
                                           )
