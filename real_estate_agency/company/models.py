from django.db import models
from django.utils.translation import ugettext_lazy as _

from real_estate.models.image import (
    BaseDraggapbleImage,
    thumbnail_factory,
    thumbnail_64_64,
    thumbnail_260_260
)


class Award(BaseDraggapbleImage):
    image_thumbnail = thumbnail_factory(320, 430)
    thumbnail_admin = thumbnail_factory(90, 120)

    def __str__(self):
        return _('грамота №%(pk)s') % {'pk': self.pk}

    class Meta:
        ordering = ['position']
        verbose_name = _('грамота')
        verbose_name_plural = _('грамоты')


class BankPartner(BaseDraggapbleImage):
    title = models.CharField(
        verbose_name=_('название банка'),
        max_length=127,
    )
    thumbnail_34_34 = thumbnail_factory(34, 34)
    thumbnail_64_64 = thumbnail_64_64
    thumbnail_260_260 = thumbnail_260_260

    class Meta:
        ordering = ('position',)
        verbose_name = _('объект банк-партнер')
        verbose_name_plural = _('банки-партнеры')
