from django.apps import AppConfig
from django.utils.translation import ugettext_lazy as _


class ApplicationsConfig(AppConfig):
    name = 'applications'
    verbose_name = _('заявки')
