from django.db import models
from django.contrib.auth.models import User
from django.core.validators import MinValueValidator
from django.utils.translation import ugettext as _

from real_estate.models import PropertyImage, Apartment
from address.models import Address


class NewApartment(Apartment):
    is_primary = True
    building = models.ForeignKey('NewBuilding',
                                 verbose_name=_('строение'),
                                 on_delete=models.CASCADE,
                                 )
    stocks = None  # Many to many fields


class NewBuilding(Address):
    """it is building with concrete address,
    but it also has a name in ResidentalComlex area
    """
    TYPE_BRICK = 'BRICK'
    TYPE_MONOLITHIC = 'MONO'
    TYPE_FRAME = 'FRAME'
    TYPE_PANEL = 'PANEL'
    TYPE_MONOLITHIC_FRAME = 'MFRAME'
    TYPE_BRICK_PANEL = 'BPANEL'
    BUILDING_TYPE_CHOICES = (
        (TYPE_BRICK, _('кирпичный')),
        (TYPE_MONOLITHIC, _('монолитный')),
        (TYPE_FRAME, _('каркасный')),
        (TYPE_PANEL, _('панельный')),
        (TYPE_MONOLITHIC_FRAME, _('монолитно-каркасный')),
        (TYPE_BRICK_PANEL, _('панельный-кирпичный')),
    )

    name = models.CharField(verbose_name=_('имя дома'),
                            max_length=127,
                            default=_('ГП'),
                            )
    residental_complex = models.ForeignKey('ResidentalComplex',
                                           verbose_name=_('ЖК'),
                                           on_delete=models.CASCADE,
                                           )
    building_type = models.CharField(max_length=127,
                                     verbose_name=_('исполнение дома'),
                                     choices=BUILDING_TYPE_CHOICES,
                                     default=TYPE_MONOLITHIC,
                                     )
    number_of_storeys = models.PositiveSmallIntegerField(
        verbose_name=_('количество этажей'),
        validators=[MinValueValidator(1)],
    )
    date_of_start_of_construction = models.DateField(verbose_name=_('дата начала стройки'),
                                                     null=True,
                                                     blank=True,
                                                     help_text=_(
        'Важен только месяц'),
    )
    date_of_construction = models.DateField(verbose_name=_('дата постройки'),
                                            null=True,
                                            blank=True,
                                            help_text=_(
                                                'Важен только месяц'),
                                            )
    feed_link = models.URLField(verbose_name=_('ссылка на фид'),
                                max_length=255,
                                null=True,
                                blank=True,
                                )
    active = models.BooleanField(verbose_name=_('отображать на сайте'),
                                 default=True,
                                 )
    def __str__(self):
        return '%s' % (self.name, )

    class Meta(Address.Meta):
        verbose_name = _('дом')
        verbose_name_plural = _('дома')
        # unique_together = ('street', 'building', 'building_block')#,


class ResidentalComplex(models.Model):
    """ it is aggregate of houses.
    They are built in the same style by the same builder.
    """
    name = models.CharField(verbose_name=_('название'),
                            max_length=127,
                            unique=True,
                            )
    description = models.TextField(verbose_name=_('описание ЖК'),)
    builder = models.ForeignKey('Builder',
                                verbose_name=_('застройщик'),
                                on_delete=models.PROTECT,
                                )
    # one to many "photos"
    characteristics = models.ManyToManyField('ResidentalComplexСharacteristic',
                                             verbose_name=_(
                                                 'характеристики ЖК'),
                                             blank=True,)
    # one to many "features"
    # one to many "houses"
    video_link = models.URLField(verbose_name=_('ссылка на видео'),
                                 null=True,
                                 blank=True,
                                 )
    presentation = models.FileField(verbose_name=_('презентация ЖК'),
                                    null=True,
                                    blank=True,
                                    )
    # one to many "documents_for_construction"
    active = models.BooleanField(verbose_name=_('отображать в новостройках'),
                                 default=False,
                                 )
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
    logo = models.ImageField(verbose_name=_('логотип компании'))

    def __str__(self):
        return self.name

    class Meta:
        verbose_name = _('застройщик')
        verbose_name_plural = _('застройщики')


class ResidentalComplexСharacteristic(models.Model):
    pass
