from django.shortcuts import render
from django.http import Http404

from dal import autocomplete

from .models import StreetModel, NeighbourhoodModel

class BaseAutocompleteForAuthenticatedUsersView(autocomplete.Select2QuerySetView):
    model = None
    
    def get_queryset(self, *args):
        if not self.request.user.is_authenticated() or not self.model:
            raise Http404()

        qs = self.model.objects.all()

        if self.q:
            qs = qs.filter(name__icontains=self.q)
        return qs


class StreetAutocompleteView(BaseAutocompleteForAuthenticatedUsersView):
    model = StreetModel


class NeighbourhoodAutocompleteView(BaseAutocompleteForAuthenticatedUsersView):
    model = NeighbourhoodModel