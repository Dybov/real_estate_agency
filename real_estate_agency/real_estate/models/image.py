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
