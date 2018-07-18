from django.db import models
from django.core.validators import MinValueValidator
from django.utils.translation import ugettext as _

from address.models import BaseAddressNoNeighbourhood, NeighbourhoodMixin


class BaseBuildingWithoutNeighbourhood(BaseAddressNoNeighbourhood):
    # Type of building material
    TYPE_BRICK = 'BRICK'
    TYPE_MONOLITHIC = 'MONO'
    TYPE_FRAME = 'FRAME'
    TYPE_PANEL = 'PANEL'
    TYPE_MONOLITHIC_FRAME = 'MFRAME'
    TYPE_BRICK_PANEL = 'BPANEL'
    TYPE_REINFORCED_CONCRETE_BLOCKS = 'RCBLOCK'
    TYPE_SILICAT_BLOCK = "SBLOCK"
    BUILDING_TYPE_CHOICES = (
        (TYPE_BRICK, _('кирпичный')),
        (TYPE_MONOLITHIC, _('монолитный')),
        (TYPE_FRAME, _('каркасный')),
        (TYPE_PANEL, _('панельный')),
        (TYPE_MONOLITHIC_FRAME, _('монолитно-каркасный')),
        (TYPE_BRICK_PANEL, _('панельный-кирпичный')),
        (TYPE_REINFORCED_CONCRETE_BLOCKS, _('блоки железобетоные')),
        (TYPE_SILICAT_BLOCK, _('cиликатный блок')),
    )
    building_type = models.CharField(max_length=127,
                                     verbose_name=_('исполнение дома'),
                                     choices=BUILDING_TYPE_CHOICES,
                                     default=TYPE_MONOLITHIC,
                                     )
    number_of_storeys = models.PositiveSmallIntegerField(
        verbose_name=_('количество этажей'),
        validators=[MinValueValidator(1)],
        default=1,
    )

    class Meta(BaseAddressNoNeighbourhood.Meta):
        verbose_name = _('дом')
        verbose_name_plural = _('дома')
        abstract = True


class BaseBuilding(BaseBuildingWithoutNeighbourhood, NeighbourhoodMixin):
    class Meta(BaseBuildingWithoutNeighbourhood.Meta):
        abstract = True
