from decimal import Decimal

from django.db import models
from django.core.validators import MinValueValidator
from django.utils.translation import ugettext as _

from .property import BasePropertyModel


class Apartment(BasePropertyModel):
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
    rooms = models.CharField(
        max_length=1,
        choices=ROOMS_CHOICES,
        default=ONEROOM,
        verbose_name=_('количество комнат'),
        help_text=(
            'Если вы не нашли нужного пункта - обратитесь к администратору'
        ),
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
                                       )],
                                       blank=True, null=True,
                                       )

    def __str__(self):
        if self.rooms == self.BACHELOR:
            return _("квартира-студия")
        return _("{rooms_integer}-комнатная квартира").format(
            rooms_integer=self.rooms
        )

    class Meta:
        abstract = True
        verbose_name = _('объект "квартира"')
        verbose_name_plural = _('квартиры')
