from decimal import Decimal

from django.db import models
from django.contrib.auth.models import User
from django.core.validators import MinValueValidator
from django.utils.translation import ugettext as _

# from address.models import Address, BaseUniqueModel


class PropertyImage(models.Model):
    #property = models.ForeignKey('BasePropertyModel', related_name='images')
    image = models.ImageField(verbose_name='изображения')
    def __str__(self):
        return _('изображение')
    class Meta:
        abstract =True
        verbose_name='файл'
        verbose_name_plural='файлы'



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

    # columns of the table
    # address = models.ForeignKey(Address,
    #                             on_delete=models.PROTECT,
    #                             verbose_name=_('адрес'),
    #                             )
    total_area = models.DecimalField(_('общая площадь (м2)'),
                                     decimal_places=2,
                                     max_digits=5,
                                     validators=[MinValueValidator(
                                                 Decimal('10.00')
                                                 ),
                                                 ],
                                     )
    description = models.TextField(verbose_name=_('описание'))
    # one to many to "images" - will be tabular inline in admin
    # many to many "layout" (image) - will be tabular inline in admin too
    celling_height = models.DecimalField(_('высота потолка (м)'),
                                         decimal_places=1,
                                         max_digits=2,
                                         validators=[MinValueValidator(
                                                     Decimal('2.0')
                                                     ),
                                                     ],
                                         )
    interior_decoration = models.CharField(verbose_name=_('вид отделки'),
                                           max_length=31,
                                           choices=INTERIOR_DECORATION_CHOICES,
                                           default=UNFURNISHED,
                                           )
    # many to many "transactions" for future releases
    price = models.DecimalField(verbose_name=_('цена, рб'),
                                default=1000000,
                                decimal_places=0,
                                max_digits=15,
                                validators=[MinValueValidator(
                                            Decimal('0.0')
                                            ),
                                            ],
                                )
    is_active = models.BooleanField(verbose_name=_('доступно на рынке'),
                                    default=True,
                                    )
    posted_by = models.ForeignKey(User,
                                  verbose_name=_('разместил'),
                                  editable=False,
                                  default=None,
                                  null=True,
                                  on_delete=models.SET_DEFAULT,
                                  )
    date_added = models.DateTimeField(auto_now_add=True)
    last_modification = models.DateTimeField(auto_now=True)
    def __str__(self):
        return "%s_%s" %(self.TYPE,self.id)
        return "%s по адресу %s" % (self.TYPE.capitalize(), self.address)
    class Meta:
        abstract = True
        verbose_name = _('объект недвижимости')
        verbose_name_plural = _('объекты недвижимости')

# https://djbook.ru/rel1.8/ref/forms/validation.html#cleaning-and-validating-fields-that-depend-on-each-other

class Apartment(BasePropertyModel):#, BaseUniqueModel):
    TYPE = 'Apartment'
    BACHELOR = 'B'
    ONEROOM  = '1'
    TWOROOM  = '2'
    THREEROOM  = '3'
    FOURROOM = '4'
    ROOMS_CHOICES = (
            (BACHELOR, _('студия')),
            (ONEROOM, _('1')),
            (TWOROOM, _('2')),
            (THREEROOM, _('3')),
            (FOURROOM, _('4')),
        )
    is_primary = False
    apartment_number = models.IntegerField(verbose_name=_('Номер квартиры'))
    rooms = models.CharField(max_length=1,
                             choices=ROOMS_CHOICES,
                             default=ONEROOM,
                             verbose_name=_('количество комнат'),
                             help_text=_('Если вы не нашли нужного пункта - обратитесь к администратору'),
                             )
    floor   = models.PositiveIntegerField(verbose_name=_('этаж'), default=1)

    class Meta:
        abstract = True
        verbose_name = _('квартиры')
        verbose_name_plural  = _('квартиры')
