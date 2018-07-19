import datetime

from django import forms
from django.db import models
from django.forms import widgets
from django.utils.translation import ugettext as _

from .helpers import last_day_of_month, get_quarter

from address.forms import FormWithAddressAutocomplete


# it is new sizes for widgets in Inlines
standart_formfield_overrides = {
    models.ManyToManyField: {'widget': forms.CheckboxSelectMultiple},
}


def SETTLEMENT_CHOICES():
    yield ('', _('Не важно'))
    today = datetime.date.today()
    yield (today.strftime("%Y-%m-%d"), _('Дом сдан'))

    QUARTER_1 = 1
    QUARTER_2 = 2
    QUARTER_3 = 3
    QUARTER_4 = 4
    QUARTERS = (QUARTER_1, QUARTER_2, QUARTER_3, QUARTER_4)
    years = [today.year, today.year + 1, today.year + 2]
    for optgroup in years:
        optgroup_choices = []
        for QUARTER in QUARTERS:
            date_of_settlement = last_day_of_month(
                datetime.date(int(optgroup), QUARTER * 3, 1))
            if date_of_settlement < today:
                continue
            optgroup_choices.append(
                (
                    date_of_settlement.strftime("%Y-%m-%d"),
                    (_("%(number_of_quarter)s квартал %(year)s") % {
                        'number_of_quarter': QUARTER,
                        'year': optgroup})
                )
            )
        yield (str(optgroup), optgroup_choices)


class SearchForm(forms.Form):
    ROOMS_CHOICES = (
        ('0', _('С')),
        ('1', '1'),
        ('2', '2'),
        ('3', '3'),
        ('4', '4+'),
    )
    price_from = forms.DecimalField(
        widget=forms.TextInput(
            attrs={'placeholder': _('от'), 'class': 'auto-numeric-currency', }
        ),
        required=False,
    )
    price_to = forms.DecimalField(
        widget=forms.TextInput(
            attrs={'placeholder': _('до'), 'class': 'auto-numeric-currency', }
        ),
        required=False,
    )
    area_from = forms.DecimalField(
        widget=forms.TextInput(
            attrs={'placeholder': _('от'), 'class': 'auto-numeric-area', }),
        required=False,
    )
    area_to = forms.DecimalField(
        widget=forms.TextInput(
            attrs={'placeholder': _('до'), 'class': 'auto-numeric-area', }),
        required=False,
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
        quarters += [
            (
                qrtr, _('{qrtr} квартал').format(qrtr=qrtr)
            ) for qrtr in range(1, 5)
        ]
        _widgets = (
            widgets.Select(attrs=attrs, choices=quarters),
            # widgets.Select(attrs=attrs, choices=years),
            widgets.NumberInput(attrs={'min': 2000, 'max': 2050}),
        )
        super(DateSelectorWidget, self).__init__(_widgets, attrs)

    def decompress(self, value):
        if value:
            return [get_quarter(value)['quarter'], value.year]
        return [None, None]

    def format_output(self, rendered_widgets):
        return ''.join(rendered_widgets)

    def value_from_datadict(self, data, files, name):
        datelist = [
            widget.value_from_datadict(data, files, name + '_%s' % i)
            for i, widget in enumerate(self.widgets)]

        try:
            D = last_day_of_month(
                datetime.date(
                    day=1,
                    month=int(datelist[0]) * 3,
                    year=int(datelist[1])
                ))
        except Exception:
            return None
        else:
            return D


class NewBuildingForm(FormWithAddressAutocomplete):
    date_of_construction = forms.DateField(
        widget=DateSelectorWidget(),
        help_text=_(
            'выберите квартал, впишите год'),
        label=_('дата окончания постройки'),
        required=False,
    )
    date_of_start_of_construction = forms.DateField(
        widget=DateSelectorWidget(),
        help_text=_(
            'выберите квартал, впишите год'),
        label=_('дата начала стройки'),
        required=False,
    )


class ResidentalComplexForm(FormWithAddressAutocomplete):

    class Media:
        js = ['real_estate/js/jquery.min.js',
              'js/collapsed_stacked_inlines.js', ]
