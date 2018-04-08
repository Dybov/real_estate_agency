from django.apps import AppConfig
from django.utils.translation import ugettext_lazy as _


class AddressConfig(AppConfig):
    name = 'address'
    verbose_name = _('адреса')
