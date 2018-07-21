from django.shortcuts import render
from django.shortcuts import get_object_or_404
from django.views.generic import ListView
from django.views.generic.edit import FormMixin

from .models import ResaleApartment
from .forms import ResaleSearchForm


class ResaleListView(FormMixin, ListView):
    form_class = ResaleSearchForm
    model = ResaleApartment
    context_object_name = 'apartments'
    template_name = 'resale/resale_list.html'
    queryset = model.objects.filter(is_active=True, )


def detailed(request, pk):
    context = {'apartment': get_object_or_404(ResaleApartment, pk=pk)}
    return render(request, 'resale/resale_detailed.html', context)
