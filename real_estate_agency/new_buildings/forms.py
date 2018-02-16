import datetime

from django import forms
from django.db import models
from django.contrib.admin import TabularInline, StackedInline
from django.contrib.admin.widgets import AdminFileWidget
from django.forms import widgets
from django.forms.widgets import (TextInput,
                                  NumberInput,
                                  Textarea,
                                  SelectMultiple,
                                  ClearableFileInput,
                                  )
from django.utils.safestring import mark_safe
from django.utils.translation import ugettext as _

from .models import ResidentalComplexImage, ResidentalComplex, NewBuilding
from .helpers import last_day_of_month, get_quarter

from address.forms import FormWithAddressAutocomplete


# it is new sizes for widgets in Inlines
standart_formfield_overrides = {
    # Changed because of using StackedInline insead of Tabular
    # models.CharField: {'widget': TextInput(attrs={'size': '10'})},
    # models.PositiveSmallIntegerField: {'widget': NumberInput(attrs={'size': '3'})},
    # models.IntegerField: {'widget': NumberInput(attrs={'style': 'width:6ch', })},
    # models.DecimalField: {'widget': NumberInput(attrs={'style': 'width:6ch', })},
    # models.TextField: {'widget': Textarea(attrs={'cols': 80, 'rows': 3})},
    models.ManyToManyField: {'widget': forms.CheckboxSelectMultiple},
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


class StackedInlineWithImageWidgetInline(StackedInline, TabularInlineWithImageWidgetInline):
    image_fields = []

    def formfield_for_dbfield(self, db_field, **kwargs):
        return super(StackedInlineWithImageWidgetInline, self).formfield_for_dbfield(db_field, **kwargs)
    # def formfield_for_dbfield(self, db_field, **kwargs):
    #     if db_field.name in self.image_fields:
    #         request = kwargs.pop("request", None)
    #         kwargs['widget'] = AdminThumbnailImageWidget
    #         return db_field.formfield(**kwargs)
    # return super(StackedInlineWithImageWidgetInline,
    # self).formfield_for_dbfield(db_field, **kwargs)


class PhotoAdminForm(forms.ModelForm):

    class Meta:
        model = ResidentalComplexImage
        widgets = {'image': ClearableFileInput(attrs={'multiple': True})}
        fields = '__all__'

    def save(self, *args, **kwargs):
        """ Override for multiupload images """
        from django.utils.datastructures import MultiValueDict

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

            self.files = MultiValueDict(
                {image_name_initial: self.files.getlist(image_name)})
            self.data[rc_name_initial] = self.data[rc_name]
            #self.data['id_'+rc_name_initial] = self.data[rc_name]
            self.data[id_initial] = self.data[id_]
        files_list = self.files.getlist(image_name_initial)

        # If multiupload
        if len(files_list)>1:
            for file in files_list:
                print(file)
                new_form = PhotoAdminForm(
                    self.data,
                    MultiValueDict(
                        {image_name_initial: [file]}),
                )
                if new_form.is_valid():
                    # print('file valid', file)
                    answer = new_form.save()
                else:
                    print('file invalid', file)
                    for field in new_form:
                        print(field)
                        for error in field.errors:
                            print(error)
                            pass
                    print(new_form.non_field_errors())
        else:
            answer = super().save(*args, **kwargs)
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

    QUARTER_1 = 1
    QUARTER_2 = 2
    QUARTER_3 = 3
    QUARTER_4 = 4
    QUARTERS = (QUARTER_1, QUARTER_2, QUARTER_3, QUARTER_4)

    for optgroup in ("2018", "2019", "2020"):
        optgroup_choices = []
        for QUARTER in QUARTERS:
            optgroup_choices.append(
                (
                    # QUARTER,
                    last_day_of_month(datetime.date(int(optgroup), QUARTER*3, 1)).strftime("%Y-%m-%d"),
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


class DateSelectorWidget(widgets.MultiWidget):

    def __init__(self, attrs=None):
        # create choices for quarters and years
        # years = [(year, year) for year in (2011, 2012, 2013)]
        quarters = [(None, '---'), ]
        quarters += [(qrtr, _('{qrtr} квартал').format(qrtr=qrtr))
                    for qrtr in range(1, 5)]
        _widgets = (
            widgets.Select(attrs=attrs, choices=quarters),
            # widgets.Select(attrs=attrs, choices=years),
            widgets.NumberInput(attrs={'min': 2000, 'max': 2050}),
        )
        super(DateSelectorWidget, self).__init__(_widgets, attrs)

    def decompress(self, value):
        if value:
            return [get_quarter(value)['quarter'], value.year]
        return [None, None] # datetime.datetime.now().year]

    def format_output(self, rendered_widgets):
        return ''.join(rendered_widgets)

    def value_from_datadict(self, data, files, name):
        datelist = [
            widget.value_from_datadict(data, files, name + '_%s' % i)
            for i, widget in enumerate(self.widgets)]
        
        try:
            D = last_day_of_month(datetime.date(day=1, month=int(datelist[0])*3,
                                                year=int(datelist[1])))
        except:
            return None
        else:
            return D


class NewBuildingForm(FormWithAddressAutocomplete):
    date_of_construction = forms.DateField(widget=DateSelectorWidget(), 
                                           help_text=_(
                                            'выберите квартал, впишите год'),
                                           label=_('дата окончания постройки'),
                                           required=False,
                                           )
    date_of_start_of_construction = forms.DateField(widget=DateSelectorWidget(), 
                                                    help_text=_(
                                                     'выберите квартал, впишите год'),
                                                    label=_('дата начала стройки'),
                                                    required=False,
                                                    )

class ResidentalComplexForm(FormWithAddressAutocomplete):

    class Media:
        js = ['real_estate/js/jquery.min.js',
              'js/collapsed_stacked_inlines.js', ]
