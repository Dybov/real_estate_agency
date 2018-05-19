from django.forms import ModelForm

from address.forms import address_fields_widgets
from new_buildings.apps import NewBuildingsConfig as rc_app_config
from .models import ResaleApartment

from dal import autocomplete

widgets = address_fields_widgets.copy()
widgets.update({'residental_complex': autocomplete.ModelSelect2(url='%s:rc-autocomplete' % rc_app_config.name)})

class ResaleApartmentForm(ModelForm):
    class Meta:
        fields = '__all__'
        # exclude = ('zip_code','coordinates',)
        model = ResaleApartment
        widgets = widgets