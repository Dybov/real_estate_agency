from django.apps import AppConfig
from django.utils.translation import ugettext_lazy as _

class RealEstateConfig(AppConfig):
    name = 'real_estate'
    verbose_name=_('Недвижимость')