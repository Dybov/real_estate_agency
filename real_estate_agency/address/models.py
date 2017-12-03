from django.db import models
from django.utils.translation import ugettext as _
from django.core.validators import MinValueValidator
from django.core.exceptions import ObjectDoesNotExist, ValidationError

class BaseUniqueModel(models.Model):
    ITS_CLASSES = []

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

        if not self in BaseUniqueModel.ITS_CLASSES:
            BaseUniqueModel.ITS_CLASSES.append(self)

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

            # that is Andrew Dybov part for checking unique fields in inline forms
            for its_cls in BaseUniqueModel.ITS_CLASSES:
                if its_cls == self:
                    continue
                other_forms_fields_status = []
                for field_name in field_tuple:
                    other_forms_fields_status.append(
                        getattr(its_cls, field_name) == getattr(
                            self, field_name)
                    )
                if set(other_forms_fields_status) == set([True]):
                    # clean it for blocking recursive errors for all post
                    # requests
                    BaseUniqueModel.ITS_CLASSES = [its_cls]
                    its_cls.raiseValidationErrorUnique(unique_fields)
                    self.raiseValidationErrorUnique(unique_fields)
            # end of Andrew Dybov part

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



# for now city is always Tyumen
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

    def __str__(self):
        return self.full_address

    @property
    def full_address(self):
        address = _('{street}, {building}').format(street=self.street, building=self.building)
        if self.building_block:
            address += _('/{block}').format(block=self.building_block)
        return address

    class Meta:
        abstract = True
        unique_together = (('street', 'building', 'building_block', ), )#'city'),)


class AbstractAddressModel(AbstractAddressModelWithoutNeighbourhood):
    neighbourhood = models.ForeignKey(NeighbourhoodModel,
                                      verbose_name=_('район'),
                                      on_delete=models.PROTECT,
                                      )
    class Meta(AbstractAddressModelWithoutNeighbourhood.Meta):
        pass
