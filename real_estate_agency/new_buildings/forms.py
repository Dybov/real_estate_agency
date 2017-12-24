import datetime

from django import forms
from django.db import models
from django.contrib.admin import TabularInline
from django.contrib.admin.widgets import AdminFileWidget
from django.forms.widgets import (TextInput,
                                  NumberInput,
                                  Textarea,
                                  SelectMultiple,
                                  ClearableFileInput,
                                  )
from django.utils.safestring import mark_safe
from django.utils.translation import ugettext as _

from .models import ResidentalComplexImage, ResidentalComplex, NewBuilding


# it is new sizes for widgets in Inlines
standart_formfield_overrides = {
    models.CharField: {'widget': TextInput(attrs={'size': '10'})},
    models.PositiveSmallIntegerField: {'widget': NumberInput(attrs={'size': '3'})},
    models.IntegerField: {'widget': NumberInput(attrs={'style': 'width:6ch', })},
    models.DecimalField: {'widget': NumberInput(attrs={'style': 'width:6ch', })},
    models.TextField: {'widget': Textarea(attrs={'cols': 80, 'rows': 3})},
}


class AdminThumbnailImageWidget(AdminFileWidget):
    ''' it base widget which allows to show loaded image near to the 'browse' button '''

    def render(self, name, value, attrs=None):
        output = []
        if value and getattr(value, "url", None):
            image_url = value.url
            file_name = str(value)
            output.append(u'<br><a href="%s" target="_blank"><img src="%s" alt="%s"  width=150/></a><br>' %
                          (image_url, image_url, file_name))
        output.append(super(AdminFileWidget, self).render(name, value, attrs))
        return mark_safe(u''.join(output))


class TabularInlineWithImageWidgetInline(TabularInline):
    ''' it is inline which allows to show loaded image near to the 'browse' button into it'''
    # image_fields - fields which images will be shown in admin
    image_fields = []

    def formfield_for_dbfield(self, db_field, **kwargs):
        if db_field.name in self.image_fields:
            request = kwargs.pop("request", None)
            kwargs['widget'] = AdminThumbnailImageWidget
            return db_field.formfield(**kwargs)
        return super(TabularInlineWithImageWidgetInline, self).formfield_for_dbfield(db_field, **kwargs)


class PhotoAdminForm(forms.ModelForm):

    class Meta:
        model = ResidentalComplexImage
        widgets = {'image': ClearableFileInput(attrs={'multiple': True})}
        fields = '__all__'

    def save(self, *args, **kwargs):
        from django.utils.datastructures import MultiValueDict
        """ Override for multiupload images """

        # Set output names in forms and formsets
        image_name_initial = 'image'
        image_name = image_name_initial

        rc_name_initial = 'residental_complex'
        rc_name = rc_name_initial

        id_initial = 'id'
        id_ = id_initial

        # For formsets
        if self.prefix:
            image_name = "%s-%s" % (self.prefix, image_name)
            rc_name = "%s-%s" % (self.prefix, rc_name)
            id_ = "%s-%s" % (self.prefix, id_)
        
            self.files = MultiValueDict({image_name_initial:self.files.getlist(image_name)})
            self.data[rc_name_initial] = self.data[rc_name]
            #self.data['id_'+rc_name_initial] = self.data[rc_name]
            self.data[id_initial] = self.data[id_]

        files_list = self.files.getlist(image_name_initial)
        answer = super().save(*args, **kwargs)
        
        if len(files_list) > 1:
            files_list.pop()

            img = self.cleaned_data.get(image_name)
            # For saving each file from multiupload
            new_form = PhotoAdminForm(self.data, self.files)
            # new_form.image = self.files.get(image_name)
            if new_form.is_valid():
                new_form.save()
            else:
                for field in new_form:
                    print(field)
                    for error in field.errors:
                        print(error)
                print(new_form.non_field_errors())
                # Breaks if not valid image
                return
        return answer


params_for_decimal_from = {"min_value": 0,
                           "decimal_places": 1, 'required': False}
params_for_decimal_to = params_for_decimal_from.copy()

params_for_decimal_from['widget'] = forms.NumberInput(
    attrs={'placeholder': _('от')})
params_for_decimal_to['widget'] = forms.NumberInput(
    attrs={'placeholder': _('до')})


def SETTLEMENT_CHOICES():
    yield ('', _('Не важно'))
    yield (datetime.date.today(), _('Уже'))

    def last_day_of_month(any_day):
        next_month = any_day.replace(
            day=28) + datetime.timedelta(days=4)  # this will never fail
        return next_month - datetime.timedelta(days=next_month.day)

    QUARTER_1 = 1
    QUARTER_2 = 2
    QUARTER_3 = 3
    QUARTER_4 = 4
    QUARTERS = (QUARTER_1, QUARTER_2, QUARTER_3, QUARTER_4)

    for optgroup in (2018, 2019, 2020):
        optgroup_choices = []
        for QUARTER in QUARTERS:
            optgroup_choices.append(
                (
                    last_day_of_month(datetime.date(optgroup, QUARTER*3, 1)),
                    (_("%(number_of_quarter)s квартал %(year)s") % {'number_of_quarter': QUARTER,
                                                                    'year': optgroup})
                )
            )
        yield (optgroup, optgroup_choices)


class SearchForm(forms.Form):
    ROOMS_CHOICES = (
        ('0', _('С')),
        ('1', '1'),
        ('2', '2'),
        ('3', '3'),
        ('4', '4+'),
    )
    price_from = forms.DecimalField(
        **params_for_decimal_from
    )
    price_to = forms.DecimalField(
        **params_for_decimal_to
    )
    area_from = forms.DecimalField(
        **params_for_decimal_from
    )
    area_to = forms.DecimalField(
        **params_for_decimal_to
    )
    rooms = forms.MultipleChoiceField(
        widget=forms.CheckboxSelectMultiple(attrs={
            "class": "checkbox"
        }),
        choices=ROOMS_CHOICES,
        required=False,
        help_text=_('С - студия'),
    )
    settlement_before = forms.ChoiceField(
        widget=forms.Select(attrs={
            "class": "search_form_select-select ",
        }),
        choices=SETTLEMENT_CHOICES,
        required=False,
    )
    any_text = forms.CharField(
        widget=forms.TextInput(attrs={
            "placeholder": _("Название улицы, района, или жилого комплекса"),
            "class": "search_place_input ",
        }
        ),
        required=False,
    )
