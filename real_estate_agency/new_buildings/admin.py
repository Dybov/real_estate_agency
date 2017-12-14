from django.db import models
from django.contrib import admin
from django.utils.translation import ugettext as _
from django.forms.models import BaseInlineFormSet

from real_estate.admin import DontShowInAdmin

from address.forms import FormWithAddressAutocomplete

from .forms import (TabularInlineWithImageWidgetInline,
                    standart_formfield_overrides,
                    PhotoAdminForm,
                    )
from .admin_filters import BuildingIsBuiltFilter, BuildingResidentalComplexFilter
from .models import (ResidentalComplex,
                     NewBuilding,
                     Builder,
                     NewApartment,
                     ResidentalComplexImage,
                     TypeOfComplex,
                     ResidentalComplexСharacteristic,
                     ResidentalComplexFeature,
                     )

admin.site.register(Builder)
admin.site.register(TypeOfComplex)
admin.site.register(ResidentalComplexСharacteristic)


class NewApartmentInline(TabularInlineWithImageWidgetInline):
    model = NewApartment
    extra = 0
    exclude = ['description']
    # image_fields will be inline
    image_fields = ['layout']
    formfield_overrides = standart_formfield_overrides
    # if it will be registred then show link
    show_change_link = True


@admin.register(NewBuilding)
class BuildingAdmin(DontShowInAdmin):
    # class BuildingAdmin(admin.ModelAdmin):
    form = FormWithAddressAutocomplete
    inlines = [NewApartmentInline]
    list_display = ['__str__', 'is_built', 'residental_complex']
    empty_value_display = _('Неизвестно')
    list_filter = [BuildingIsBuiltFilter, BuildingResidentalComplexFilter]
    initial_exclude = ['zip_code', 'feed_link', ]
    exclude = initial_exclude + ['residental_complex']


class BuildingInline(admin.TabularInline):
    form = FormWithAddressAutocomplete
    model = NewBuilding
    extra = 0
    exclude = BuildingAdmin.initial_exclude + ['is_active']
    formfield_overrides = standart_formfield_overrides
    show_change_link = True


class ResidentalComplexImageInline(admin.TabularInline):
    model = ResidentalComplexImage
    form = PhotoAdminForm
    extra = 0
    min_num = 0


class ResidentalComplexFeatureInline(admin.TabularInline):
    model = ResidentalComplexFeature
    extra = 0
    min_num = 0
    formfield_overrides = standart_formfield_overrides


@admin.register(ResidentalComplex)
class ResidentalComplexAdmin(admin.ModelAdmin):
    form = FormWithAddressAutocomplete
    inlines = [ResidentalComplexFeatureInline,
               BuildingInline,
               ResidentalComplexImageInline,
               ]
    list_display = ('name', 'is_active')
    list_editable = ('is_active',)
    list_filter = ['is_active']
    search_fields = ['name']
    filter_horizontal = ['characteristics']
    fieldsets = (
        (None, {
            'fields': ('type_of_complex', 'name', 'neighbourhood', 'is_active', 'is_popular', 'builder', 'characteristics', 'number_of_flats')
        }),
        (_('ДОКУМЕНТЫ'), {
            'fields': ('building_permit', 'project_declarations'),
        }),
        (_('МЕДИА'), {
            'fields': ('front_image', 'video_link', 'presentation'),
        }),
    )


@admin.register(ResidentalComplexImage)
class PhotoOfResidentalComplexAdminTemporary(admin.ModelAdmin):
    form = PhotoAdminForm
