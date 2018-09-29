from django.db import models
from django.utils.translation import ugettext_lazy as _

from . import get_file_path

from .image import spec_factory


class Characteristic(models.Model):
    characteristic = models.CharField(
        verbose_name=_('характеристика'),
        max_length=127,
        unique=True,
    )
    icon = models.ImageField(verbose_name=_('иконка'),
                             upload_to=get_file_path,
                             )
    thumbnail = spec_factory(52, 52, source='icon',)

    def __str__(self):
        return self.characteristic

    class Meta:
        verbose_name = _('характеристика')
        verbose_name_plural = _('характеристики')
