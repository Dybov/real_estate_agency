from django.db import models
from django.utils.translation import ugettext as _

from real_estate.models import get_file_path, BasePropertyImage


class Award(BasePropertyImage):
    position = models.PositiveSmallIntegerField(default=0,
                                                verbose_name=_('позиция'))
    def __str__(self):
        return _('грамота №%(pk)s') % {'pk':self.pk}

    class Meta:
        ordering = ['position']
        verbose_name = _('грамота')
        verbose_name_plural = _('грамоты')
