from django.db import models
from django.utils.translation import ugettext as _

from new_buildings.models import ResidentalComplex
from real_estate.models import get_file_path


class Feedback(models.Model):
    author = models.CharField(verbose_name=_('клиент'),
                              max_length=127,
                              )
    bought = models.ForeignKey(ResidentalComplex,
                               verbose_name=_('где купили'),
                               )
    message = models.TextField(verbose_name=_('текст отзыва'))
    work_at = models.CharField(verbose_name=_('место работы'),
                               max_length=127,
                               blank=True,
                               null=True,
                               )
    image = models.ImageField(verbose_name=_('фото'),
                              upload_to=get_file_path)
    is_active = models.BooleanField(verbose_name=_('отображать на сайте'),
                                    default=True,
                                    )

    def __str__(self):
        return _("{author} из {company}").format(author=self.author, company=self.work_at)

    class Meta:
        verbose_name = _('отзыв')
        verbose_name_plural = _('отзывы')
