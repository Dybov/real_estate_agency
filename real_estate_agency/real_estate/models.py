from decimal import Decimal

from django.db import models
from django.contrib.auth.models import User
from django.core.validators import MinValueValidator
# Prepare for future translations and localizations:
from django.utils.translation import ugettext as _

from address.models import BaseAddressNoNeighbourhood, NeighbourhoodMixin

def get_file_path(instance, filename):
    """Gets file name for uploaded files
    Specific folder uses app_name, model_name
    Also used uuid number for file_name
    uuid - (https://en.wikipedia.org/wiki/Universally_unique_identifier)
    """
    import uuid
    app = instance._meta.app_label
    model_name = instance._meta.model_name
    id_ = instance.id
    ext = filename.split('.')[-1]
    filename = "%s.%s" % (uuid.uuid4(), ext)
    return 'uploads/%s/%s/%s/%s' % (app, model_name, ext, filename)


# Decorator for overriding part of the field in model subclasses
# Source https://stackoverflow.com/questions/927729/how-to-override-the-verbose-name-of-a-superclass-model-field-in-django
def modify_fields(**kwargs):
    def wrap(cls):
        for field, prop_dict in kwargs.items():
            for prop, val in prop_dict.items():
                setattr(cls._meta.get_field(field), prop, val)
        return cls
    return wrap


class BasePropertyImage(models.Model):
    """Abstract model for all real estate pictures
    Helps to use django inlines with pictures.
    """
    image = models.ImageField(verbose_name='изображение',
                              upload_to=get_file_path)

    def __str__(self):
        return _('изображение')

    class Meta:
        abstract = True
        verbose_name = _('изображение')
        verbose_name_plural = _('изображения')


class BasePropertyModel(models.Model):
    """Base class (multi-table) for all real estate objects"""
    TYPE = None
    # types of the interior decoration
    DESIGNED = 'D'
    EURO_DESIGN = 'ED'
    FURNISHED = 'F'
    SEMI_FURNISHED = 'SF'
    PREPARED_FOR_FURNISHING = 'P'
    UNFURNISHED = 'UF'
    INTERIOR_DECORATION_CHOICES = ((DESIGNED, _('ремонт')),
                                   (EURO_DESIGN, _('евро ремонт')),
                                   (FURNISHED, _('чистовая')),
                                   (SEMI_FURNISHED, _('предчистовая')),
                                   (PREPARED_FOR_FURNISHING,
                                    _('улучшенная черновая')),
                                   (UNFURNISHED, _('черновая')),
                                   )
    layout = models.ImageField(verbose_name='планировка',
                               upload_to=get_file_path,
                               )
    total_area = models.DecimalField(_('общая площадь (м2)'),
                                     decimal_places=2,
                                     max_digits=5,
                                     validators=[MinValueValidator(
                                                 Decimal('15.00')
                                                 ),
                                                 ],
                                     )
    interior_decoration = models.CharField(verbose_name=_('вид отделки'),
                                           max_length=31,
                                           choices=INTERIOR_DECORATION_CHOICES,
                                           default=UNFURNISHED,
                                           )
    price = models.DecimalField(verbose_name=_('цена, рб'),
                                default=1000000,
                                decimal_places=0,
                                max_digits=15,
                                validators=[MinValueValidator(
                                            Decimal('0.0')
                                            ),
                                            ],
                                )
    description = models.TextField(verbose_name=_('описание'),
                                   blank=True,
                                   null=True,
                                   )
    celling_height = models.DecimalField(_('высота потолка (м)'),
                                         decimal_places=1,
                                         max_digits=2,
                                         default=2.7,
                                         validators=[MinValueValidator(
                                                     Decimal('2.0')
                                                     ),
                                                     ],
                                         )
    is_active = models.BooleanField(verbose_name=_('отображать на сайте'),
                                    default=True,
                                    )
    created_by = models.ForeignKey(User,
                                   verbose_name=_('создано'),
                                   default=None,
                                   null=True,
                                   on_delete=models.SET_DEFAULT,
                                   related_name="%(app_label)s_%(class)s_created",
                                   )
    modified_by = models.ForeignKey(User,
                                    verbose_name=_('изменено'),
                                    default=None,
                                    null=True,
                                    on_delete=models.SET_DEFAULT,
                                    related_name="%(app_label)s_%(class)s_modified",
                                    )
    date_added = models.DateTimeField(verbose_name=_('добавлено'),
                                      auto_now_add=True,
                                      )
    last_modification = models.DateTimeField(verbose_name=_('изменено'),
                                             auto_now=True,
                                             )

    # need to add: one to many to "images" - will be tabular inline in admin
    @property
    def images(self):
        raise NotImplementedError

    @property
    def price_per_square_meter(self):
        return self.price/self.total_area 

    # many to many "transactions" will be added in future releases and will
    # replace the price
    def __str__(self):
        return "%s_%s" % (self.TYPE, self.id)
        return "%s по адресу %s" % (self.TYPE.capitalize(), self.address)

    class Meta:
        abstract = True
        verbose_name = _('объект недвижимости')
        verbose_name_plural = _('объекты недвижимости')


class Apartment(BasePropertyModel):  # , BaseUniqueModel):
    TYPE = 'Apartment'
    BACHELOR = 'B'
    ONEROOM = '1'
    TWOROOMS = '2'
    THREEROOMS = '3'
    FOURROOMS = '4'
    FIVEROOMS = '5'
    SIXROOMS = '6'
    SEVENROOMS = '7'
    ROOMS_CHOICES = (
        (BACHELOR, _('студия')),
        (ONEROOM, _('1')),
        (TWOROOMS, _('2')),
        (THREEROOMS, _('3')),
        (FOURROOMS, _('4')),
        (FIVEROOMS, _('5')),
        (SIXROOMS, _('6')),
        (SEVENROOMS, _('7')),
    )
    is_primary = False
    rooms = models.CharField(max_length=1,
                             choices=ROOMS_CHOICES,
                             default=ONEROOM,
                             verbose_name=_('количество комнат'),
                             help_text=_(
                                 'Если вы не нашли нужного пункта - обратитесь к администратору'),
                             )
    floor = models.CharField(verbose_name=_('этаж'), 
                             default=1,
                             max_length=127)
    section = models.PositiveIntegerField(verbose_name=_('подъезд/секция'),
                                          validators=[MinValueValidator(1)],
                                          default=1)
    kitchen_area = models.DecimalField(_('площадь кухни (м2)'),
                                       default=5,
                                       decimal_places=2,
                                       max_digits=5,
                                       validators=[MinValueValidator(
                                           Decimal('5.00')
                                       ),
    ],
    )
    balcony_area = models.DecimalField(verbose_name=_('площадь балкона (м2)'),
                                       default=0,
                                       decimal_places=2,
                                       max_digits=5,
                                       validators=[MinValueValidator(
                                           Decimal('0.00')
                                           )
                                       ],
                                       blank=True, null=True,
                                       )

    def __str__(self):
        if self.rooms == self.BACHELOR:
            return _("квартира-студия")
        return _("{rooms_integer}-комнатная квартира").format(rooms_integer=self.rooms)

    class Meta:
        abstract = True
        verbose_name = _('объект "квартира"')
        verbose_name_plural = _('квартиры')


class BaseBuildingWithoutNeighbourhood(BaseAddressNoNeighbourhood):
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
    building_type = models.CharField(max_length=127,
                                     verbose_name=_('исполнение дома'),
                                     choices=BUILDING_TYPE_CHOICES,
                                     default=TYPE_MONOLITHIC,
                                     )
    number_of_storeys = models.PositiveSmallIntegerField(
        verbose_name=_('количество этажей'),
        validators=[MinValueValidator(1)],
        default=1,
    )
    class Meta(BaseAddressNoNeighbourhood.Meta):
        verbose_name = _('дом')
        verbose_name_plural = _('дома')
        abstract = True

class BaseBuilding(BaseBuildingWithoutNeighbourhood, NeighbourhoodMixin):
    class Meta(BaseBuildingWithoutNeighbourhood.Meta):
        abstract = True