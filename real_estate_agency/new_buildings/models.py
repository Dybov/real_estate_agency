from django.db import models
from django.contrib.auth.models import User
from django.utils.translation import ugettext as _

from real_estate.models import PropertyImage, Apartment
#from address import Address


class NewApartment(Apartment):  # , BaseUniqueModel):
    is_primary = True

# class Building(Address):


class Building(models.Model):
    """it is building with concrete address,
    but it also has a name in ResidentalComlex area
    """
    name = models.CharField(verbose_name=_('имя дома'),
                            max_length=127,
                            default=_('ГП'),
                            )
    residental_complex = models.ForeignKey('ResidentalComplex',
                                           verbose_name=_('ЖК'),
                                           default=None,
                                           blank=True,
                                           null=True,
                                           on_delete=models.CASCADE,
                                           )

    def __str__(self):
        return '%s' % (self.name, )

    class Meta:
        verbose_name = _('дом')
        verbose_name_plural = _('дома')


class ResidentalComplex(models.Model):
    """ it is aggregate of houses.
    They are built in the same style by the same builder.
    """
    name = models.CharField(verbose_name=_('название'),
                            max_length=127,
                            unique=True,
                            )
    active = models.BooleanField(verbose_name=_('отображать в новостройках'),
                                 default=False,
                                 )
    builder = models.ForeignKey('Builder',
                                verbose_name=_('застройщик'),
                                on_delete=models.PROTECT,
                                )
    # ?nearestplaces
    # one to many "photos"
    # many to many "features"
    # one to one "characteristics"
    # one to many "houses"
    # presentation = models.FileField()

    # def lowest_price(self):
    #     from django.db.models import Min
    #     if not self.address_set:
    #         return 0
    #     addresses = self.address_set.all()
    #     if len(addresses)==0:
    #         return
    #     minimums = []
    #     for address in addresses:
    #         _property = address.property_set.all()
    #         if _property:
    #             minimum = _property.annotate(Min('price'))[0].price
    #             minimums.append(minimum)
    #     return min(minimums)
    def __str__(self):
        return self.name

    class Meta:
        verbose_name = _('жилой комплекс')
        verbose_name_plural = _('жилые комплексы')


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
    contact = models.ForeignKey(User,
                                on_delete=models.PROTECT,
                                verbose_name=_('контактное лицо'),
                                )
    image = models.ImageField(verbose_name=_('логотип компании'))

    def __str__(self):
        return self.name
