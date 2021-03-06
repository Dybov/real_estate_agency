from django.contrib import admin
from django.utils.translation import ugettext_lazy as _

from adminsortable2.admin import SortableInlineAdminMixin

from real_estate.admin import (
    AdminInlineImages,
    MultiuploadInlinesContainerMixin,
)

from .models import (
    ResaleApartment,
    ResaleApartmentImage,
    ResaleCharacteristic,
    ResaleDecoration,
)
from .forms import ResaleApartmentForm, ResaleApartmentImageForm


class ResaleImageInline(
        SortableInlineAdminMixin, admin.TabularInline, AdminInlineImages):
    model = ResaleApartmentImage
    form = ResaleApartmentImageForm
    classes = ['collapse', ]
    extra = 0
    min_num = 0
    fields = ('thumbnail', 'image')
    readonly_fields = ('thumbnail', )


@admin.register(ResaleApartment)
class ResaleApartmentAdmin(MultiuploadInlinesContainerMixin, admin.ModelAdmin):
    inlines = [ResaleImageInline, ]
    form = ResaleApartmentForm

    list_display_initial = (
        'id', 'status', 'is_active', 'rooms', 'total_area',
        'full_price', 'agency_price', 'fee', 'price',
        'residental_complex',
    )

    list_filter_initial = ('rooms', 'residental_complex', )

    list_display = list_display_initial
    list_filter = list_filter_initial
    list_display_links = (
        'id', 'status', 'rooms', 'total_area'
    )
    list_editable = ('is_active', )
    readonly_fields = ['id', 'date_added', 'modified_by']
    filter_horizontal = ['characteristics']

    def fee(self, obj):
        return obj.fee
    fee.short_description = _('комиссия')

    def full_price(self, obj):
        return obj.full_price
    full_price.short_description = _("текущая стоимость")

    fieldsets = None

    # For multiupload by MultiuploadInlinesContainerMixin
    related_inline_form = ResaleApartmentImageForm
    related_inline_fk = 'apartment'

    def get_fieldsets(self, request, obj=None):
        self.fieldsets = self.dynamic_fieldset(request)
        return super().get_fieldsets(request, obj)

    def dynamic_fieldset(self, request):
        """
        get the dynamic field sets
        """
        deal_status_part_fields = (
            'date_added',
            ('sold_date', 'previous_buy_date',),
            'status',
            'amount_of_owners',
            'comment',
            'related_mortgage',
            'price',
            'agency_price',
            'agency_price_with_sales',
        )
        if request.user.has_perm('resale.can_add_change_delete_all_resale'):
            deal_status_part_fields += ('created_by', 'modified_by',)
        deal_status_part = (_('Информация по сделке'), {
            'classes': ('collapse',),
            'fields': deal_status_part_fields,
        })

        owner_part = (_('Информация по продавцу'), {
            'classes': ('collapse',),
            'fields': (('owner_name', 'owner_phone_number'),),
        })

        apartment_part_fields = (
            'neighbourhood',
            'residental_complex',
            'street',
            (
                'building',
                'building_block',
            ),
            'coordinates',
            'rooms',
            (
                'floor',
                'number_of_storeys',
            ),
            'section',
            'apartment_number',
            'building_type',
            'home_series',
            'date_of_construction',
            (
                'total_area',
                'kitchen_area',
                'balcony_area',
            ),
            (
                'celling_height',
                'decoration',
            ),
            'layout',
            'description',
            'characteristics'
        )
        apartment_part = (_('Информация по квартире'), {
            'classes': ('collapse',),
            'fields': apartment_part_fields,
        })

        fieldsets = (
            (None, {
                'fields': ('id', 'is_active',),
            }),
            deal_status_part,
            owner_part,
            apartment_part,
        )

        return fieldsets

    def save_model(self, request, obj, form, change):
        super().save_model(request, obj, form, change)
        # Auto set user
        if not change:
            obj.created_by = request.user
        if 'modified_by' not in form.changed_data:
            obj.modified_by = request.user
        obj.save()

    def get_queryset(self, request):
        qs = super(ResaleApartmentAdmin, self).get_queryset(request)
        if request.user.has_perm('resale.can_add_change_delete_all_resale'):
            return qs
        return qs.filter(created_by=request.user)

    def changelist_view(self, request, extra_context=None):
        self.list_display = self.list_display_initial
        self.list_filter = self.list_filter_initial
        if request.user.has_perm('resale.can_add_change_delete_all_resale'):
            self.list_display += ('created_by',)
            self.list_filter = ('created_by',) + self.list_filter
        return super(ResaleApartmentAdmin, self).changelist_view(
            request, extra_context)


admin.site.register(ResaleCharacteristic)
admin.site.register(ResaleDecoration)
