from django import forms
from django.utils.translation import ugettext as _


class SearchForm(forms.Form):
    """Form for searching resale apartmnents
    It search by the next fields:
    rooms [char choice] - amount of rooms in apartment
    price_from [decimal] - minimal apartment price
    price_to [decimal] - maximal apartment price
    area_from [decimal] - minimal apartment area
    area_to [decimal] - maximal apartment area
    any_text [string] - name of street, neighbourhood or RC
    """
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
    any_text = forms.CharField(
        widget=forms.TextInput(attrs={
            "placeholder": _("Название улицы, района, или жилого комплекса"),
            "class": "search_place_input ",
        }
        ),
        required=False,
    )
