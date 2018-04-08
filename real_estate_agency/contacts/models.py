from django.db import models
from django.utils.translation import ugettext_lazy as _


class SocialLinkType(models.Model):
    name = models.CharField(max_length=256,
                            verbose_name=_('название соц сети'),
                            )
    symbol = models.CharField(max_length=256,
                              verbose_name=_('символ в кодировке шрифтов'),
                              blank=True,
                              )

    image = models.ImageField(upload_to='social_media_links',
                              verbose_name=_('иконка'),
                              null=True, blank=True,
                              )
    # For ordering 
    position = models.IntegerField(verbose_name=_('порядок при стандартной сортировке'),
                                   blank=True, null=True,
                                   )
    def __str__(self):
        return self.name

    class Meta:
        verbose_name = 'тип соц сети'
        verbose_name_plural = 'типы соц сетей'
        ordering = ['position']

class SocialLink(models.Model):
    link_type = models.ForeignKey(SocialLinkType,
                                  verbose_name=_('соц сеть'),
                                  )

    name = models.CharField(max_length=256,
                            verbose_name=_('отображаемый текст на ссылке'),
                            blank=True,
                            )

    url = models.CharField(max_length=4000,
                           verbose_name=_('ссылка'),
                           )

    title = models.CharField(max_length=512,
                             verbose_name=_('заголовок тэга'),
                             blank=True,
                             )

    def __str__(self):
        return self.name

    def get_img(self):
        return self.link_type.image

    def get_type(self):
        return self.link_type.name

    class Meta:
        verbose_name = 'соц сеть'
        verbose_name_plural = 'соц сети'
        ordering = ['link_type__position']
        abstract = True