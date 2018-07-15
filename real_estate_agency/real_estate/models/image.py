from django.db import models
from django.utils.translation import ugettext as _

from .helper import get_file_path


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
