from datetime import date

from django.forms import (
    ModelForm,
    NumberInput,
    DateField,
    ModelChoiceField,
    Select
)
from django.forms.widgets import ClearableFileInput
from django.core.validators import MinValueValidator, MaxValueValidator
from django.utils.translation import ugettext_lazy as _

from dal import autocomplete

from address.forms import address_fields_widgets
from address.models import NeighbourhoodModel
from applications.forms import RussianPhoneNumberFormMixin
from new_buildings.apps import NewBuildingsConfig as rc_app_config
from real_estate.forms import SearchForm

from .models import ResaleApartment, ResaleApartmentImage


MIN_YEAR = 1850


class SimpleSelectYearWidget(NumberInput):
    def value_from_datadict(self, data, files, name):
        value = data.get(name, '')
        if value:
            value = date(year=int(value), month=1, day=1)
        return value

    def format_value(self, value):
        if value:
            # str is needed for localization which may convert 1850 -> 1 850
            return str(value.year)
        return None


resale_widgets = address_fields_widgets.copy()
resale_widgets.update({
    'residental_complex': autocomplete.ModelSelect2(
        url='%s:rc-autocomplete' % rc_app_config.name),
    'date_of_construction': SimpleSelectYearWidget(
        attrs={
            # str is needed for localization which may convert 1850 -> 1 850
            'min': str(MIN_YEAR),
            'max': str(date.today().year)
        },
    ),
})


class ResaleApartmentForm(RussianPhoneNumberFormMixin, ModelForm):
    PHONE_NUMBER_FIELD = 'owner_phone_number'

    class Meta:
        fields = '__all__'
        model = ResaleApartment
        widgets = resale_widgets
    date_of_construction = DateField(
        label=_('Год постройки дома'),
        widget=SimpleSelectYearWidget(),
        required=False,
        validators=[
            MaxValueValidator(
                date.today(),
                message=_(
                    'убедитесь, что год постройки дома не больше текущего года'
                )
            ),
            MinValueValidator(
                date(year=MIN_YEAR, month=1, day=1),
                message=_(
                    'убедитесь, что год постройки дома не меньше %(year)s года'
                ) % {'year': MIN_YEAR}
            ),
        ],
    )


class ResaleApartmentImageForm(ModelForm):
    class Meta:
        model = ResaleApartmentImage
        fields = '__all__'
        widgets = {'image': ClearableFileInput(attrs={'multiple': True})}


class ResaleSearchForm(SearchForm):
    """Form for searching resale apartmnents
    It search by the next fields:
    rooms [char choice] (from SearchForm) - amount of rooms in apartment
    price_from [decimal] (from SearchForm) - minimal apartment price
    price_to [decimal] (from SearchForm) - maximal apartment price
    area_from [decimal] (from SearchForm) - minimal apartment area
    area_to [decimal] (from SearchForm) - maximal apartment area
    any_text [string] (from SearchForm) - name of street, neighbourhood or RC
    neighbourhood [choice FK] - name of the neighbourhood
    """
    neighbourhood = ModelChoiceField(
        queryset=NeighbourhoodModel.objects.exclude(resaleapartment=None),
        empty_label=_('Не важно'),
        widget=Select(attrs={
            "class": "search_form_select-select ",
        }),
        required=False,
    )
