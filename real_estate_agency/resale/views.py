from django.shortcuts import render
from django.http import Http404
from django.views.generic import ListView
from django.views.generic.edit import FormMixin

from rest_framework.renderers import JSONRenderer

from real_estate.views import ApartmentFilterMixin

from .models import ResaleApartment, TransactionMixin
from .forms import ResaleSearchForm
from .serializers import ResaleApartmentSerializer


class ResaleListView(ApartmentFilterMixin, FormMixin, ListView):
    form_class = ResaleSearchForm
    model = ResaleApartment
    context_object_name = 'apartments'
    template_name = 'resale/resale_list.html'
    # Recude DB connections with select_related()
    queryset = model.objects.filter(
        is_active=True, status=TransactionMixin.ACTIVE).select_related()

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
    # Recude DB connections with select_related()
    # Don't use get_object_or_404 to have possibility use select_related()
    apartments = ResaleApartment.objects.filter(
        pk=pk).select_related().prefetch_related('photos')
    if not apartments:
        raise Http404("Apartment doesn't exist")
    apartment = apartments[0]

    # Serialize apartment data to use it in React JS
    # In the fututre rest API will provide json
    data = ResaleApartmentSerializer(apartment).data
    apartment_json = JSONRenderer().render(data).decode('utf-8')
    agent = apartment.created_by.get_instance_or_default()

    context = {
        'apartment': apartment,
        'apartment_json': apartment_json,
        'agent': agent,
    }
    return render(request, 'resale/resale_detailed.html', context)
