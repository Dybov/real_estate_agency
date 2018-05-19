from django.contrib import admin
from django.utils.translation import ugettext_lazy as _

from .models import ResaleApartment
from .forms import ResaleApartmentForm


@admin.register(ResaleApartment)
class ResaleApartmentAdmin(admin.ModelAdmin):
    form = ResaleApartmentForm
    list_display = ('id', 'rooms', 'total_area', 'agency_price', 'fee', 'price', 'residental_complex')

    def fee(self, obj):
        return obj.fee
    fee.short_description = _('комиссия')

    fieldsets = (
        (_('Информация по квартире'), {
            'fields': ('rooms',
                       'is_active',
                       'price',
                       'agency_price',
                       'floor',
                       'total_area',
                       'kitchen_area',
                       'balcony_area',
                       'description',
                       'layout',
                       'interior_decoration',
                       'celling_height',
                       )
        }),
        (_('Информация о доме'), {
            'fields': ('neighbourhood',
                       'street',
                       'building',
                       'building_block',
                       'coordinates',
                       'residental_complex'),
        }),
    )