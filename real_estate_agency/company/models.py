from django.db import models
from django.utils.translation import ugettext as _

from real_estate.models import BasePropertyImage

from imagekit.models.fields import ImageSpecField
from imagekit.processors import ResizeToFit, ResizeToFill


class Award(BasePropertyImage):
    position = models.PositiveSmallIntegerField(default=0,
                                                verbose_name=_('позиция'))
    image_thumbnail = ImageSpecField(
        processors=[
            ResizeToFit(
                320,
                430,
                mat_color=(255, 255, 255, 1)
            )
        ],
        source='image',
        format='JPEG',
        options={
            'quality': 60,
            'progressive': True,
        }
    )

    def __str__(self):
        return _('грамота №%(pk)s') % {'pk': self.pk}

    class Meta:
        ordering = ['position']
        verbose_name = _('грамота')
        verbose_name_plural = _('грамоты')
