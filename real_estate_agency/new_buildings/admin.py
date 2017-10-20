from datetime import date

from django.db import models
from django.contrib import admin
from django.utils.html import format_html
from django.forms.widgets import  TextInput, NumberInput, Textarea
from django.utils.translation import ugettext as _
from django.contrib.admin.widgets import AdminFileWidget
from django.utils.safestring import mark_safe
from .models import ResidentalComplex, NewBuilding, Builder, NewApartment
from real_estate.admin import DontShowInAdmin

standart_formfield_overrides = {
    models.CharField: {'widget': TextInput(attrs={'size':'10'})},
    models.PositiveSmallIntegerField: {'widget': NumberInput(attrs={'size':'3'})},
    models.IntegerField: {'widget': NumberInput(attrs={'style': 'width:6ch',})},
    models.DecimalField: {'widget': NumberInput(attrs={'style': 'width:12ch',})},
    models.TextField: {'widget': Textarea(attrs={'cols': 1, 'rows': 2})},
}


class AdminImageWidget(AdminFileWidget):

    def render(self, name, value, attrs=None):
        output = []
        if value and getattr(value, "url", None):
            image_url = value.url
            file_name = str(value)
            output.append(u'<br><a href="%s" target="_blank"><img src="%s" alt="%s"  width=150/></a><br>' %
                          (image_url, image_url, file_name))
        output.append(super(AdminFileWidget, self).render(name, value, attrs))
        return mark_safe(u''.join(output))


class ImageWidgetAdmin(admin.TabularInline):
    image_fields = []

    def formfield_for_dbfield(self, db_field, **kwargs):
        if db_field.name in self.image_fields:
            request = kwargs.pop("request", None)
            kwargs['widget'] = AdminImageWidget
            return db_field.formfield(**kwargs)
        return super(ImageWidgetAdmin, self).formfield_for_dbfield(db_field, **kwargs)


class NewApartmentAdmin(ImageWidgetAdmin):
    model = NewApartment
    extra = 0
    image_fields = ['layout']
    formfield_overrides = standart_formfield_overrides
    show_change_link = True #if it will be refistred

class BuildingIsBuiltFilter(admin.SimpleListFilter):
    # descriptions is here https://docs.djangoproject.com/en/dev/ref/contrib/admin/#django.contrib.admin.ModelAdmin.list_filter
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


class BuildingResidentalComplexFilter(admin.SimpleListFilter):
    # descriptions is here https://docs.djangoproject.com/en/dev/ref/contrib/admin/#django.contrib.admin.ModelAdmin.list_filter
    title = _('ЖК')
    parameter_name = 'residental-complex'

    def lookups(self, request, model_admin):
        return ResidentalComplex.objects.values_list('id', 'name')
        return (
            ('ready', _('Построен')),
            ('not-ready', _('Строится')),
        )

    def queryset(self, request, queryset):
        if self.value():
            return queryset.filter(id=self.value())



class BuildingAdmin(admin.ModelAdmin):
    inlines = [NewApartmentAdmin]
    list_display = ['__str__', 'is_built', 'residental_complex']
    empty_value_display = _('Неизвестно')
    list_filter = [BuildingIsBuiltFilter, BuildingResidentalComplexFilter]
    initial_exclude = ['city', 'country', 'zip_code', 'feed_link',]
    exclude =  initial_exclude + ['residental_complex']

class BuildingInline(admin.TabularInline):
    model = NewBuilding
    extra = 0
    exclude = BuildingAdmin.initial_exclude + ['active']
    formfield_overrides = standart_formfield_overrides
    show_change_link = True


@admin.register(ResidentalComplex)
class ResidentalComplexAdmin(admin.ModelAdmin):
    inlines = [BuildingInline, ]
    list_display = ('name', 'active')
    list_editable = ('active',)
    list_filter = ['active']
    search_fields = ['name']


admin.site.register(Builder)
admin.site.register(NewBuilding, BuildingAdmin)
