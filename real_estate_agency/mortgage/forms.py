from django import forms
from django.utils.translation import ugettext as _


class MortgageForm(forms.Form):
    full_price = forms.DecimalField(
        label=_('Цена недвижимости, руб'),
        min_value=300000,
        decimal_places=1,
        widget =forms.NumberInput(attrs={'step': 10000}),
    )
    initial_fee_percentage = forms.DecimalField(
        label=_('Первоначальный взнос, %'),
        min_value=0,
        max_value=100,
        decimal_places=1,
    )
    years = forms.IntegerField(
        label=_('Срок кредитования, г'),
        min_value=5,
        max_value=30,
    )
