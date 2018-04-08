from django.db import models
from django.utils.translation import ugettext as _

from phonenumber_field.modelfields import PhoneNumberField


class CallbackRequest(models.Model):
    name = models.CharField(_('имя'), max_length=127, blank=True, null=True)
    phone_number = PhoneNumberField(verbose_name=_('телефон'))
    url_from = models.URLField(_('источник заявки'))
    extra_info = models.CharField(
        _('дополнительная информация'), max_length=1024, blank=True, null=True)
    date = models.DateTimeField(_('время подачи'), auto_now=True)
    promotion_context = models.CharField(
        _('реклама'), max_length=127, blank=True, null=True)

    class Meta:
        verbose_name = _('обратный звонок')
        verbose_name_plural = _('заявки на обратный звонок')
