from django.shortcuts import render
from django.shortcuts import get_object_or_404
from django.views.generic import ListView
from django.views.generic.edit import FormMixin

from real_estate.views import ApartmentFilterMixin

from .models import ResaleApartment, TransactionMixin
from .forms import ResaleSearchForm


class ResaleListView(ApartmentFilterMixin, FormMixin, ListView):
    form_class = ResaleSearchForm
    model = ResaleApartment
    context_object_name = 'apartments'
    template_name = 'resale/resale_list.html'
    queryset = model.objects.filter(
        is_active=True, status=TransactionMixin.ACTIVE)

    def get(self, request, *args, **kwargs):
        data = getattr(request, request.method)

        form_class = self.get_form_class()
        self.form = form_class(data)
        self.object_list = self.get_queryset()
        self.apartment_list = self.object_list
        empty_list_flag = False

        if data and self.form.is_valid():
            self.standartApartmentFilter()

            if self.apartment_list:
                self.object_list = self.apartment_list
            else:
                empty_list_flag = True

        context = self.get_context_data(
            form=self.form,
            empty_list_flag=empty_list_flag,
        )
        return self.render_to_response(context)

    def standartApartmentFilter(self):
        # Standart filters for rooms, total_area and price
        super(ResaleListView, self).standartApartmentFilter()

        # Any text filter searches for:
        # neighbourhood, residental_complex and street
        self.aparmentByAnyTextIContains(
            fieldname='any_text',
            model_fields=[
                'neighbourhood__name',
                'residental_complex__name',
                'street__name',
            ],
        )

        # Searches for neighbourhood
        self.filterApartment(fieldname='neighbourhood',
                             filter_name='neighbourhood')


def detailed(request, pk):
    context = {'apartment': get_object_or_404(ResaleApartment, pk=pk)}
    return render(request, 'resale/resale_detailed.html', context)
