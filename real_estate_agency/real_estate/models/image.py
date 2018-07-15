from django.db import models
from django.utils.translation import ugettext as _

from imagekit.models.fields import ImageSpecField
from imagekit.processors import ResizeToFit, ResizeToFill

from .helper import get_file_path


def thumbnail_factory(
    width=16, height=16, source='image', to_fit=True, *args, **kwargs
):
    """ Abstract factory for ImageSpecField with default thumbnail params"""
    if to_fit:
        main_processor = ResizeToFit(
            width,
            height,
            mat_color=(255, 255, 255, 0)
        )
    else:
        main_processor = ResizeToFill(
            width,
            height,
        )
    return ImageSpecField(
        processors=[
            main_processor,
        ] + kwargs.pop('extra_processors', []),
        source=source,
        format=kwargs.pop('format', 'PNG'),
        options={
            'quality': kwargs.pop('options__quality', 50),
            'progressive': kwargs.pop('options__progressive', True),
        }
    )


thumbnail_16_16 = thumbnail_factory()
thumbnail_32_32 = thumbnail_factory(32, 32)
thumbnail_64_64 = thumbnail_factory(64, 64)
thumbnail_120_120 = thumbnail_factory(120, 120)
thumbnail_260_260 = thumbnail_factory(260, 260)


class BasePropertyImage(models.Model):
    """Abstract model for all real estate pictures
    Helps to use django inlines with pictures.
    """
    image = models.ImageField(verbose_name=_('изображение'),
                              upload_to=get_file_path)

    def __str__(self):
        return _('изображение')

    class Meta:
        abstract = True
        verbose_name = _('изображение')
        verbose_name_plural = _('изображения')


class BaseDraggapbleImage(BasePropertyImage):
    """Abstract model for all real estate pictures with ordering
    Helps to use django inlines with pictures.
    """
    position = models.PositiveIntegerField(
        verbose_name=_('позиция'),
        default=0,
        blank=False,
        null=False,
    )

    class Meta:
        abstract = True
        ordering = ('position',)

    def save(self, *args, **kwargs):
        model = self.__class__

        if self.position is None:
            # Append
            try:
                last = model.objects.order_by('-position')[0]
                self.position = last.position + 1
            except IndexError:
                # First row
                self.position = 0

        return super(BaseDraggapbleImage, self).save(*args, **kwargs)
