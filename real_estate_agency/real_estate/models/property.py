from decimal import Decimal

from django.db import models
from django.conf import settings
from django.core.validators import MinValueValidator
from django.utils.translation import ugettext as _

from address.models import BaseAddressNoNeighbourhood, AbstractAddressModel

from .helper import get_file_path


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
    created_by = models.ForeignKey(
        settings.AUTH_USER_MODEL,
        verbose_name=_('создано'),
        default=None,
        null=True,
        on_delete=models.SET_DEFAULT,
        related_name="%(app_label)s_%(class)s_created",
    )
    modified_by = models.ForeignKey(
        settings.AUTH_USER_MODEL,
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
        return self.full_price / self.total_area

    @property
    def full_price(self):
        """Must be implement atleast for price_per_square_meter.
        Cause in different types of real estate property can be:
        self.price!=self.full_price
        for example for price with agency fee
        """
        raise NotImplementedError

    # many to many "transactions" will be added in future releases and will
    # replace the price
    def __str__(self):
        return "%s_%s" % (self.TYPE, self.id)
        return "%s по адресу %s" % (self.TYPE.capitalize(), self.address)

    class Meta:
        abstract = True
        verbose_name = _('объект недвижимости')
        verbose_name_plural = _('объекты недвижимости')
