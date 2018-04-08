from django.apps import AppConfig
from django.utils.translation import ugettext_lazy as _


class NewBuildingsConfig(AppConfig):
    name = 'new_buildings'
    verbose_name = _('новостройки')

    def ready(self):
        import new_buildings.signals
