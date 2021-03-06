from django.db import models
from django.utils.translation import ugettext_lazy as _

from real_estate.models.image import (
    BaseDraggapbleImage,
    spec_factory,
    thumbnail_64_64,
    thumbnail_260_260
)


class Award(BaseDraggapbleImage):
    image_thumbnail = spec_factory(320, 430)
    thumbnail_admin = spec_factory(90, 120)

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
    thumbnail_34_34 = spec_factory(34, 34)
    thumbnail_64_64 = thumbnail_64_64
    thumbnail_260_260 = thumbnail_260_260

    def __str__(self):
        return self.title

    class Meta:
        ordering = ('position',)
        verbose_name = _('объект банк-партнер')
        verbose_name_plural = _('банки-партнеры')
