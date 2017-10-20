from django.db import models
from django.utils.translation import ugettext as _
from django.core.validators import MinValueValidator


class BaseUniqueModel(models.Model):
    class Meta:
        abstract = True
    def clean(self):
        """
        Check for instances with null values in unique_together fields.
        from https://stackoverflow.com/questions/3488264/django-unique-together-doesnt-work-with-foreignkey-none/4805581#4805581
        """
        from django.core.exceptions import ValidationError

        super(BaseUniqueModel, self).clean()

        for field_tuple in self._meta.unique_together[:]:
            unique_filter = {}
            unique_fields = []
            null_found = False
            for field_name in field_tuple:
                field_value = getattr(self, field_name)
                if getattr(self, field_name) is None:
                    unique_filter['%s__isnull' % field_name] = True
                    null_found = True
                else:
                    unique_filter['%s' % field_name] = field_value
                    unique_fields.append(field_name)
            if null_found:
                unique_queryset = self.__class__.objects.filter(
                    **unique_filter
                )
                if self.pk:
                    unique_queryset = unique_queryset.exclude(pk=self.pk)
                if unique_queryset.exists():
                    msg = self.unique_error_message(
                        self.__class__, tuple(unique_fields))
                    raise ValidationError(msg)


class Address(BaseUniqueModel):
    # Countries choices. For now only Russia
    RUSSIA = 'RU'
    COUNTRY_CHOICES = (
        (RUSSIA, _('Россия')),
    )
    # Cities choices. For now only Tyumen
    TYUMEN = 'RU-TMN'
    CITY_CHOICES = (
        (TYUMEN, _('Тюмень')),
    )

    # Neighbourhood choices. It will depends on City object, when business will grow
    MMS = 'MMS'
    MYS = 'MYS'
    NEIGHBOURGOOD_CHOICES = (
        (MMS, _('ММС')),
        (MYS, _('Мыс')),
    )
    country = models.CharField(verbose_name=_('страна'),
                               max_length=127,
                               choices=COUNTRY_CHOICES,
                               default=RUSSIA,
                               )
    city = models.CharField(verbose_name=_('город'),
                            max_length=127,
                            choices=CITY_CHOICES,
                            default=TYUMEN,
                            )
    neighbourhood = models.CharField(verbose_name=_('район'),
                                   max_length=127,
                                   choices=NEIGHBOURGOOD_CHOICES,
                                   )
    street = models.CharField(verbose_name=_('улица'),
                              max_length=127,
                              )
    building = models.IntegerField(verbose_name=_('дом'),
                                   validators=[MinValueValidator(1)]
                                   )
    building_block = models.IntegerField(verbose_name=_('корпус'),
                                         null=True,
                                         blank=True,
                                         validators=[MinValueValidator(1)],
                                         help_text=_('оставьте пустым, если поле не имеет смысла'),
                                         )
    zip_code = models.CharField(verbose_name=_('почтовый индекс'),
                                max_length=127,
                                null=True,
                                blank=True,
                                )

    def __str__(self):
        return self.full_address

    @property
    def full_address(self):
        address = _('Ул. %s, д. %s.') % (self.street, self.building)
        if self.building_block:
            address += _('/%s') % (self.building_block)
        return address

    class Meta:
        abstract = True
        unique_together = (('street', 'building', 'building_block'),) # for future also - 'country','city',