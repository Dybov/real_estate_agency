from django.apps import AppConfig
from django.utils.translation import ugettext_lazy as _


class ResaleConfig(AppConfig):
    name = 'resale'
    verbose_name = _('каталог квартир')
