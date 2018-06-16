from decimal import Decimal

from django.core.exceptions import ValidationError
from django.core.validators import MinValueValidator
from django.core.urlresolvers import reverse
from django.db import models
from django.utils.translation import ugettext_lazy as _

from imagekit.models.fields import ImageSpecField
from imagekit.processors import ResizeToFit

from company.views import BANK_PARTNERS
from real_estate.models import (
    Apartment,
    BaseBuilding,
    modify_fields,
    get_file_path,
    BasePropertyImage
)
from new_buildings.models import ResidentalComplex


# Defined to add feature in the future
class ResaleWatermark(object):
    def process(self, image):
        return image


class TransactionMixin(models.Model):
    ACTIVE = 'ACTIVE'
    SOLD_WITH_US = 'SOLD-BY-US'
    SOLD_WITHOUT_US = 'SOLD-BY-SMBD'
    STATUS_CHOICES = ((ACTIVE, _('активна')),
                      (SOLD_WITH_US, _('продано с помощью ДОМУС')),
                      (SOLD_WITHOUT_US, _('продано без участия ДОМУС')),
                      )
    status = models.CharField(verbose_name=_('статус сделки'),
                              max_length=127,
                              choices=STATUS_CHOICES,
                              default=ACTIVE,
                              )
    comment = models.TextField(verbose_name=_('комментарий/результат сделки'),
                               blank=True,
                               null=True,
                               )
    sold_date = models.DateField(
        verbose_name=_('дата продажи/завершения сделки'),
        blank=True,
        null=True,
    )
    previous_buy_date = models.DateField(
        verbose_name=_(
            'дата предыдущей покупки/сделки по данной недвижимости'),
        blank=True,
        null=True,
    )
    # revenue =

    class Meta:
        abstract = True


@modify_fields(price={
    'verbose_name': ('цена от продавца, рб'),
    'help_text': _('данная цена является той суммой\n, которую хочет получить продавец.\
      Не отображается на сайте.')})
class ResaleApartment(Apartment, BaseBuilding, TransactionMixin):
    MORTGAGE_CHOICES = tuple((v, k,) for k, v in BANK_PARTNERS.items())
    agency_price = models.DecimalField(
        verbose_name=_('цена с комиссией от агенства, рб'),
        default=1000000,
        decimal_places=0,
        max_digits=15,
        validators=[MinValueValidator(
            Decimal('0.0')
        ),
        ],
        help_text=_(
            'данная цена = цена от продавца + комиссия Домус'),
    )
    residental_complex = models.ForeignKey(ResidentalComplex,
                                           verbose_name=_('жилой комплекс'),
                                           on_delete=models.SET_DEFAULT,
                                           default=None,
                                           blank=True,
                                           null=True,
                                           )
    apartment_number = models.PositiveIntegerField(
        verbose_name=_('номер квартиры'),
        validators=[
            MinValueValidator(1)],
        null=True,
        blank=True
    )
    home_series = models.CharField(verbose_name=_('серия дома'),
                                   max_length=127,
                                   null=True,
                                   blank=True)
    date_of_construction = models.DateField(
        verbose_name=_('Год постройки дома'),
        null=True,
        blank=True,
    )
    related_mortgage = models.CharField(verbose_name=_('В ипотеке у'),
                                        max_length=127,
                                        choices=MORTGAGE_CHOICES,
                                        default=None,
                                        help_text=_(
                                            'если находится в ипотеке'),
                                        null=True,
                                        blank=True,
                                        )
    amount_of_owners = models.PositiveIntegerField(
        verbose_name=_('количество собственников'),
        validators=[
            MinValueValidator(1)],
        default=1,
    )

    def clean(self):
        # Don't allow set agency_price lower than real price.
        if self.agency_price is not None \
                and self.price is not None \
                and self.agency_price < self.price:
            raise ValidationError(
                {'agency_price':
                 _('цена с комиссией от агенства %(agency_price)s \
                    должна быть больше реальной цены %(real_price)s') % {
                     'agency_price': self.agency_price,
                     'real_price': self.price
                 }
                 }
            )

    @property
    def fee(self):
        if self.agency_price and self.price:
            return self.agency_price - self.price

    @property
    def full_price(self):
        return self.agency_price

    @property
    def verbose(self):
        return self.__str__() + ', ' + self.address

    @property
    def address(self):
        return _('ул. ')+super().address

    def get_absolute_url(self):
        return reverse('resale:detailed', args=[self.pk])

    class Meta:
        verbose_name = _('объект вторичка')
        verbose_name_plural = _('объекты вторички')

    thumbnail = ImageSpecField(
        [ResizeToFit(
            400,
            300,
            mat_color=(255, 255, 255, 0)),
         ResaleWatermark(),
         ],
        source='layout',
        format='PNG',
        options={'quality': 40,
                 'progressive': True,
                 },
    )


class ResaleApartmentImage(BasePropertyImage):
    apartment = models.ForeignKey(ResaleApartment,
                                  on_delete=models.CASCADE,
                                  related_name='photos',
                                  )
