from django import forms
from django.utils.translation import ugettext as _
from django.core.exceptions import ValidationError


class MortgageForm(forms.Form):
    full_price = forms.DecimalField(
        label=_('Стоимость жилья, руб'),
        min_value=300000,
        decimal_places=1,
        widget=forms.NumberInput(attrs={'step': 1}),
    )
    initial_fee = forms.DecimalField(
        label=_('Первоначальный взнос, руб'),
        min_value=0,
        decimal_places=1,
        widget=forms.NumberInput(attrs={'step': 1}),
    )
    years = forms.IntegerField(
        label=_('Срок кредитования, г'),
        min_value=5,
        max_value=30,
    )

    def clean(self):
        cleaned_data = super().clean()
        # initial_fee must be lower than full_price
        if self.is_valid():
            initial_fee = cleaned_data.get('initial_fee')
            full_price = cleaned_data.get('full_price')
            if initial_fee >= full_price:
                raise ValidationError(
                    {'initial_fee': [
                        _('Убедитесь, что это значение меньше стоимости жилья'), ]}
                )
        return cleaned_data
