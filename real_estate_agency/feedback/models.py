from django.db import models
from django.utils.translation import ugettext as _

from new_buildings.models import ResidentalComplex
from real_estate.models.helper import get_file_path
from real_estate.models.image import spec_factory
from contacts.models import SocialLink


class Feedback(models.Model):
    author = models.CharField(
        verbose_name=_('клиент'),
        max_length=127,
    )
    residental_complex = models.ForeignKey(
        ResidentalComplex,
        verbose_name=_('ЖК'),
        blank=True,
        null=True,
    )
    is_resale = models.BooleanField(
        verbose_name=_('приобретено на вторичном рынке'),
        default=False,
    )
    date = models.DateField(
        verbose_name=_('когда совершили сделку'),
        blank=True,
        null=True,
    )
    message = models.TextField(verbose_name=_('текст отзыва'))
    work_at = models.CharField(
        verbose_name=_('место работы'),
        max_length=127,
        blank=True,
        null=True,
    )
    image = models.ImageField(
        verbose_name=_('фото'),
        upload_to=get_file_path
    )
    is_active = models.BooleanField(
        verbose_name=_('отображать на сайте'),
        default=True,
    )
    image_250_250 = spec_factory(
        250, 250,
        format='JPEG',
        options__quality=70,
        to_fit=False,
    )
    # social_media_links - one to many field

    def __str__(self):
        text = "{author}".format(
            author=self.author,
        )
        if self.work_at:
            text += _(" из {company}").format(
                company=self.work_at
            )
        return text

    def get_social_media_links(self):
        return self.social_media_links.all()

    class Meta:
        verbose_name = _('отзыв')
        verbose_name_plural = _('отзывы')
        ordering = ('-date', '-id')


class SocialLinkForFeedback(SocialLink):
    feedback = models.ForeignKey(Feedback,
                                 verbose_name=_('связанный отзыв'),
                                 related_name='social_media_links',
                                 on_delete=models.CASCADE,
                                 )
