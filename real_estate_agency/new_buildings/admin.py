from datetime import date

from django.db import models
from django.contrib import admin
from django.utils.translation import ugettext as _

from real_estate.admin import DontShowInAdmin
from .forms import TabularInlineWithImageWidgetInline, standart_formfield_overrides
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
class BuildingAdmin(admin.ModelAdmin):
    inlines = [NewApartmentInline]
    list_display = ['__str__', 'is_built', 'residental_complex']
    empty_value_display = _('Неизвестно')
    list_filter = [BuildingIsBuiltFilter, BuildingResidentalComplexFilter]
    initial_exclude = ['city', 'country', 'zip_code', 'feed_link', ]
    exclude = initial_exclude + ['residental_complex']


class BuildingInline(admin.TabularInline):
    model = NewBuilding
    extra = 0
    exclude = BuildingAdmin.initial_exclude + ['is_active']
    formfield_overrides = standart_formfield_overrides
    show_change_link = True


class ResidentalComplexImageInline(admin.TabularInline):
    model = ResidentalComplexImage
    extra = 0
    min_num = 1


class ResidentalComplexFeatureInline(admin.TabularInline):
    model = ResidentalComplexFeature
    extra = 0
    min_num = 1
    formfield_overrides = standart_formfield_overrides


@admin.register(ResidentalComplex)
class ResidentalComplexAdmin(admin.ModelAdmin):
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
            'fields': ('type_of_complex', 'name', 'is_active', 'builder', 'characteristics', 'number_of_flats')
        }),
        (_('ДОКУМЕНТЫ'), {
            'fields': ('building_permit', 'project_declarations', 'other_documents'),
        }),
        (_('МЕДИА'), {
            'fields': ('front_image', 'video_link', 'presentation'),
        })
    )


@admin.register(ResidentalComplexСharacteristic)
# DontShowInAdmin):
class ResidentalComplexСharacteristicAdmin(admin.ModelAdmin):
    pass
