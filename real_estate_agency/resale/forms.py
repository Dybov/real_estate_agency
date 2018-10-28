from datetime import date

from django.core.exceptions import ValidationError
from django.forms import (
    ModelForm,
    NumberInput,
    DateField,
    ModelChoiceField,
    Select,
    IntegerField,
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

    def __must_be_gte(
            self,
            big_price_field, low_price_field,
            set_error_to=None):
        # big_price = getattr(self, big_price_field, None)
        # low_price = getattr(self, low_price_field, None)
        big_price = self.cleaned_data.get(big_price_field)
        low_price = self.cleaned_data.get(low_price_field)

        if None in (big_price, low_price):
            return

        # [:-4] to chunk currency at the end
        big_price_name = self.fields.get(big_price_field).label[:-4]
        low_price_name = self.fields.get(low_price_field).label[:-4]

        if set_error_to is None:
            set_error_to = big_price_field

        if low_price > big_price:
            self.validation_errors[set_error_to] = \
                _('%(big_price_name)s (%(big_price)s) \
                должна быть не меньше чем \
                %(low_price_name)s (%(low_price)s)') % {
                    'big_price_name': big_price_name,
                    'big_price': big_price,
                    'low_price_name': low_price_name,
                    'low_price': low_price}

    def clean(self):
        cleaned_data = super().clean()
        if not hasattr(self, 'validation_errors'):
            self.validation_errors = {}
        # Don't allow set agency_price lower than real price.
        self.__must_be_gte('agency_price', 'price')
        # Don't allow set agency_price lower than real agency_price_with_sales.
        self.__must_be_gte('agency_price', 'agency_price_with_sales')
        # Don't allow set agency_price_with_sales lower than real price.
        self.__must_be_gte('agency_price_with_sales', 'price')

        if self.validation_errors:
            # It allows to show all errors
            raise ValidationError(self.validation_errors)
        return cleaned_data


class ResaleApartmentImageForm(ModelForm):
    position = IntegerField(required=False)

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
