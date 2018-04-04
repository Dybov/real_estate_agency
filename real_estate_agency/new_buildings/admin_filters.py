from datetime import date

from django.contrib.admin import SimpleListFilter
from django.utils.translation import ugettext as _

from .models import ResidentalComplex


class BuildingIsBuiltFilter(SimpleListFilter):
    # descriptions is here
    # https://docs.djangoproject.com/en/dev/ref/contrib/admin/#django.contrib.admin.ModelAdmin.list_filter
    title = _('Готовность дома')
    parameter_name = 'readiness'

    def lookups(self, request, model_admin):
        return (
            ('ready', _('Построен')),
            ('not-ready', _('Строится')),
        )

    def queryset(self, request, queryset):
        if self.value() == 'ready':
            return queryset.filter(date_of_construction__lte=date.today())
        if self.value() == 'not-ready':
            return queryset.filter(date_of_construction__gt=date.today())


class BuildingResidentalComplexFilter(SimpleListFilter):
    # descriptions is here
    # https://docs.djangoproject.com/en/dev/ref/contrib/admin/#django.contrib.admin.ModelAdmin.list_filter
    title = _('ЖК')
    parameter_name = 'residental-complex'

    def lookups(self, request, model_admin):
        return ResidentalComplex.objects.values_list('id', 'name')

    def queryset(self, request, queryset):
        if self.value():
            return queryset.filter(id=self.value())
