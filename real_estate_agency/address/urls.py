from django.conf.urls import url

from . import views
from .apps import AddressConfig


app_name = AddressConfig.name

urlpatterns = [
    url(r'^json/street/$', 
        views.StreetAutocompleteView.as_view(), 
        name='street-autocomplete',
    ),
    url(r'^json/neighbourhood/$', 
        views.NeighbourhoodAutocompleteView.as_view(), 
        name='neighbourhood-autocomplete',
    ),
]
