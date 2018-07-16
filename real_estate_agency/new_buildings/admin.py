from django import forms
from django.contrib import admin
from django.utils.translation import ugettext as _
from django.forms.models import BaseInlineFormSet

from imagekit.admin import AdminThumbnail

from real_estate.admin import MultiuploadInlinesContainerMixin

from .forms import (
    standart_formfield_overrides,
    NewBuildingForm,
    ResidentalComplexForm
)
from .models import (
    ResidentalComplex,
    NewBuilding,
    Builder,
    NewApartment,
    ResidentalComplexImage,
    TypeOfComplex,
    ResidentalComplexCharacteristic,
    ResidentalComplexFeature,
)

admin.site.register(Builder)
admin.site.register(TypeOfComplex)
admin.site.register(ResidentalComplexCharacteristic)


class NewApartmentInline(admin.StackedInline):
    model = NewApartment
    extra = 0
    exclude = ['description']
    formfield_overrides = standart_formfield_overrides

    fields = (
        'thumbnail',
        'layout',
        'total_area',
        'interior_decoration',
        'price',
        'celling_height',
        'is_active',
        'rooms',
        'floor',
        'section',
        'kitchen_area',
        'balcony_area',
        'buildings',
    )

    readonly_fields = ['thumbnail']
    thumbnail = AdminThumbnail(
        image_field='layout_small',
        template='admin/display_link_thumbnail.html',
    )
    thumbnail.short_description = _('миниатюра')

    # if it will be registred then show link
    show_change_link = True

    def formfield_for_manytomany(self, db_field, request, **kwargs):
        if db_field.name == "buildings":
            try:
                parent_obj_id = request.resolver_match.args[0]
                kwargs["queryset"] = NewBuilding.objects.filter(
                    residental_complex=parent_obj_id)
            except IndexError:
                pass
        return super(NewApartmentInline, self).formfield_for_foreignkey(
            db_field, request, **kwargs)


class BuildingInlineFormSet(BaseInlineFormSet):
    def clean(self):
        '''Checks if there are no two Forms
        with the same values at unique_together'''
        if any(self.errors):
            return

        unique_together_values = []
        unique_together = NewBuilding._meta.unique_together

        def checkIfUnique(_form, unique_names):
            output = []
            for val_name in unique_names:
                if type(val_name) in (tuple, list):
                    return checkIfUnique(_form, val_name)
                value = form.cleaned_data[val_name]
                output.append(value)

            if output in unique_together_values:
                if 'name' in unique_names:
                    form.add_error(
                        None, _('Поля "Имя дома" \
                            в данном жк должны быть уникальны')
                    )
                else:
                    form.add_error(None, _(
                        'Совокупность полей "Улица", "Номер дома" \
                        и "Корпус" должна быть уникальна для всех домов'))
            else:
                unique_together_values.append(output)

        for form in self.forms:
            if form.cleaned_data:
                checkIfUnique(form, unique_together)


class BuildingInline(admin.StackedInline):
    form = NewBuildingForm
    formset = BuildingInlineFormSet
    model = NewBuilding
    extra = 0
    formfield_overrides = standart_formfield_overrides
    fields = ('name',
              'street',
              'building',
              'building_block',
              'coordinates',
              'is_active',
              'building_type',
              'number_of_storeys',
              'date_of_start_of_construction',
              'date_of_construction',
              'building_permit',
              'project_declarations'
              )


class ResidentalComplexImageForm(forms.ModelForm):
    class Meta:
        model = ResidentalComplexImage
        widgets = {
            'image': forms.widgets.ClearableFileInput(attrs={'multiple': True})
        }
        fields = '__all__'


class ResidentalComplexImageInline(admin.TabularInline):
    model = ResidentalComplexImage
    form = ResidentalComplexImageForm
    extra = 0
    min_num = 0


class ResidentalComplexFeatureInline(admin.TabularInline):
    model = ResidentalComplexFeature
    extra = 0
    min_num = 0
    formfield_overrides = standart_formfield_overrides


@admin.register(ResidentalComplex)
class ResidentalComplexAdmin(
    MultiuploadInlinesContainerMixin,
    admin.ModelAdmin
):
    related_inline_form = ResidentalComplexImageForm
    related_inline_fk = 'residental_complex'
    form = ResidentalComplexForm
    inlines = [ResidentalComplexFeatureInline,
               BuildingInline,
               NewApartmentInline,
               ResidentalComplexImageInline,
               ]
    list_display = ('name', 'is_active')
    list_editable = ('is_active',)
    list_filter = ['is_active']
    search_fields = ['name']
    filter_horizontal = ['characteristics']
    fieldsets = (
        (None, {
            'fields': ('type_of_complex',
                       'name',
                       'neighbourhood',
                       'is_active',
                       'is_popular',
                       'builder',
                       'description',
                       'characteristics',
                       'number_of_buildings',
                       'number_of_flats')
        }),
        (_('МЕДИА'), {
            'fields': ('front_image', 'video_link', 'presentation'),
        }),
    )

    def get_inline_instances(self, request, obj=None):
        """Override to exclude NewApartmentInline
        from newly added forms"""
        from copy import deepcopy

        original_inlines = deepcopy(self.inlines)
        if not obj:
            self.inlines.pop(self.inlines.index(NewApartmentInline))

        answer = super().get_inline_instances(request, obj=None)
        self.inlines = original_inlines
        return answer
