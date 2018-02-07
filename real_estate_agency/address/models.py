from django.db import models
from django.utils.translation import ugettext as _
from django.utils.functional import cached_property
from django.utils.safestring import mark_safe
from django.core.validators import MinValueValidator
from django.core.exceptions import ObjectDoesNotExist, ValidationError



import geocoder


class BaseUniqueModel(models.Model):
    class Meta:
        abstract = True

    def raiseValidationErrorUnique(self, unique_fields):
        from django.core.exceptions import ValidationError
        msg = self.unique_error_message(
            self.__class__, tuple(unique_fields))
        raise ValidationError(msg)

    def clean(self):
        """
        Check for instances with null values in unique_together fields.
        from https://stackoverflow.com/questions/3488264/django-unique-together-doesnt-work-with-foreignkey-none/4805581#4805581
        """
        super(BaseUniqueModel, self).clean()

        for field_tuple in self._meta.unique_together[:]:
            unique_filter = {}
            unique_fields = []
            null_found = False
            for field_name in field_tuple:
                try:
                    field_value = getattr(self, field_name)
                except ObjectDoesNotExist:
                    break
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


# for now city is always Tyumen so define
class City(object):
    name = _('Тюмень')

# in the future add CityModel with city name and code ISO 3166-2
# NeighbourhoodModel and StreetModel must be chained with city
# django-smart-select is great desicion for that in future


class NeighbourhoodModel(models.Model):
    name = models.CharField(verbose_name=_('название района'),
                            max_length=127,
                            unique=True,
                            )

    def __str__(self):
        return self.name

    class Meta:
        verbose_name = _('район')
        verbose_name_plural = _('районы')


class StreetModel(models.Model):
    name = models.CharField(verbose_name=_('улица'),
                            max_length=127,
                            unique=True,
                            )

    def __str__(self):
        return self.name

    class Meta:
        verbose_name = _('улица')
        verbose_name_plural = _('улицы')


class AbstractAddressModelWithoutNeighbourhood(BaseUniqueModel):
    city = City()
    street = models.ForeignKey(StreetModel,
                               verbose_name=_('улица'),
                               on_delete=models.PROTECT,
                               )
    building = models.IntegerField(verbose_name=_('номер дома'),
                                   validators=[MinValueValidator(1)]
                                   )
    building_block = models.IntegerField(verbose_name=_('корпус'),
                                         null=True,
                                         blank=True,
                                         validators=[MinValueValidator(1)],
                                         help_text=_(
                                             'оставьте пустым, если поле не имеет смысла'),
                                         )
    zip_code = models.CharField(verbose_name=_('почтовый индекс'),
                                max_length=127,
                                null=True,
                                blank=True,
                                )
    coordinates = models.CharField(verbose_name=_('широта,долгота'),
                                   max_length=127,
                                   null=True,
                                   blank=True,
                                   )

    def __str__(self):
        return self.address

    @cached_property
    def coordinates_as_list(self):
        if self.coordinates:
            return self.coordinates.split(',')
        return None, None
    @cached_property
    def coordinates_as_json(self):
        import json
        return mark_safe(json.dumps(self.coordinates_as_list))


    @cached_property
    def address_short(self):
        address = _('{street}, {building}').format(
            street=self.street, building=self.building)
        return address

    @cached_property
    def address(self):
        address = self.address_short
        if self.building_block:
            address += _('/{block}').format(block=self.building_block)
        return address

    def save(self, *args, **kwargs):
        if self.pk is None:
            self.define_coordinates()
        super().save(*args, **kwargs)

    def define_coordinates(self):
        location = geocoder.yandex(self.city.name+", "+self.address)
        if location.ok:
            self.coordinates = ",".join(location.latlng) 

    class Meta:
        abstract = True
        unique_together = (('street', 'building', 'building_block', ), )


class AbstractAddressModel(AbstractAddressModelWithoutNeighbourhood):
    neighbourhood = models.ForeignKey(NeighbourhoodModel,
                                      verbose_name=_('район'),
                                      on_delete=models.PROTECT,
                                      )

    class Meta(AbstractAddressModelWithoutNeighbourhood.Meta):
        pass
