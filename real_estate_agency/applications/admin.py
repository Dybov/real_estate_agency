from django.contrib import admin

from .models import CallbackRequest
from real_estate.admin import ReadOnlyAdminMixin


@admin.register(CallbackRequest)
class CallbackRequestAdmin(ReadOnlyAdminMixin, admin.ModelAdmin):
    list_display = ('name', 'phone_number', 'date',
                    'url_from', 'extra_info')
    list_display_links = ('name', 'phone_number',)
    list_filter = ('date', 'extra_info')
    search_fields = ('name', 'phone_number')
    exclude = ('id', 'promotion_context')
