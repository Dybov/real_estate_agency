from decimal import Decimal

from django.core.exceptions import ValidationError
from django.core.validators import MinValueValidator
from django.core.urlresolvers import reverse
from django.db import models
from django.utils.translation import ugettext_lazy as _

from phonenumber_field.modelfields import PhoneNumberField

from company.models import BankPartner
from real_estate.models.apartment import Apartment
from real_estate.models.building import BaseBuilding
from real_estate.models.helper import modify_fields
from real_estate.models.image import (
    BasePropertyImage,
    spec_factory,
    BaseWatermarkProcessor)
from new_buildings.models import ResidentalComplex


# Defined to add feature in the future
class ResaleWatermark(BaseWatermarkProcessor):
    pass


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

    class Meta:
        abstract = True


@modify_fields(
    price={
        'verbose_name': _('цена от продавца, рб'),
        'help_text': _('данная цена является той суммой, которую хочет получить продавец.\
          Не отображается на сайте.'), },
    date_added={'verbose_name': _('дата размещения')},
    created_by={'verbose_name': _('сотрудник Компании')}
)
class ResaleApartment(Apartment, BaseBuilding, TransactionMixin):
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
    related_mortgage = models.ForeignKey(
        BankPartner,
        verbose_name=_('В ипотеке у'),
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
    owner_name = models.CharField(_('ФИО продавца'),
                                  max_length=127,
                                  )
    owner_phone_number = PhoneNumberField(_('номер телефона продавца'))

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
        return _('ул. ') + super().address

    def get_absolute_url(self):
        return reverse('resale:detailed', args=[self.pk])

    class Meta:
        verbose_name = _('объект вторичка')
        verbose_name_plural = _('объекты вторички')
        permissions = (
            ("can_add_change_delete_all_resale",
                _('Иммет доступ к чужим данным по вторичке')),
        )

    thumbnail = spec_factory(
        370,
        320,
        pre_processors=[ResaleWatermark()],
        source='layout',
        format='jpeg',
    )


class ResaleApartmentImage(BasePropertyImage):
    apartment = models.ForeignKey(ResaleApartment,
                                  on_delete=models.CASCADE,
                                  related_name='photos',
                                  )
    image_spec = spec_factory(
        750,
        500,
        pre_processors=[ResaleWatermark()],
        options__quality=70,
        format='jpeg'
    )