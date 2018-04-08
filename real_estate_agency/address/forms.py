import itertools

from django import forms

from dal import autocomplete

from .apps import AddressConfig


app_name = AddressConfig.name

street_autocomplete_widget = {'street': autocomplete.ModelSelect2(url='%s:street-autocomplete' % app_name)}

neighbourhood_autocomplete_widget = {'neighbourhood': autocomplete.ModelSelect2(url='%s:neighbourhood-autocomplete' % app_name),}

address_fields_widgets = street_autocomplete_widget.copy()
address_fields_widgets.update(neighbourhood_autocomplete_widget) 

class FormWithAddressAutocomplete(forms.ModelForm):
    class Meta:
        fields = ('__all__')
        widgets = address_fields_widgets