from django.contrib import admin
from django.utils.translation import ugettext as _
from django.forms.models import BaseInlineFormSet

from .forms import (
    StackedInlineWithImageWidgetInline,
    standart_formfield_overrides,
    PhotoAdminForm,
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


class NewApartmentInline(StackedInlineWithImageWidgetInline):
    model = NewApartment
    extra = 0
    exclude = ['description']
    # image_fields will be inline
    image_fields = ['layout']
    formfield_overrides = standart_formfield_overrides
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


class SomeInlineFormSet(BaseInlineFormSet):
    def save_new(self, form, commit=True):
        # Ensure the latest copy of the related instance is present on each
        # form (it may have been saved after the formset was originally
        # instantiated).
        setattr(form.instance, self.fk.name, self.instance)
        # Use commit=False so we can assign the parent key afterwards, then
        # save the object.
        pk_value = getattr(self.instance, self.fk.remote_field.field_name)
        att_name = self.fk.get_attname()

        # For the multiupload images.
        # If form won't be saved - it'll be 500 error
        # So it is better have FK field be completed when form is saved
        form.data[form.prefix + '-' +
                  att_name] = getattr(pk_value, 'pk', pk_value)
        if att_name.endswith('_id'):
            form.data[form.prefix + '-' + att_name[:-3]
                      ] = getattr(pk_value, 'pk', pk_value)

        obj = form.save(commit=False)
        setattr(obj, att_name, getattr(pk_value, 'pk', pk_value))
        if commit:
            obj.save()

        # form.save_m2m() can be called via the formset later on
        # if commit=False
        if commit and hasattr(form, 'save_m2m'):
            form.save_m2m()
        return obj

    def save_existing(self, form, instance, commit=True):
        return form.save(commit=commit)


class ResidentalComplexImageInline(admin.TabularInline):
    model = ResidentalComplexImage
    form = PhotoAdminForm
    extra = 0
    min_num = 0
    formset = SomeInlineFormSet


class ResidentalComplexFeatureInline(admin.TabularInline):
    model = ResidentalComplexFeature
    extra = 0
    min_num = 0
    formfield_overrides = standart_formfield_overrides


@admin.register(ResidentalComplex)
class ResidentalComplexAdmin(admin.ModelAdmin):
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
