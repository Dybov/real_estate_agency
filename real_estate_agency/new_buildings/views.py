import json
import re
from statistics import median

from django.shortcuts import Http404
from django.views.generic import ListView, DetailView
from django.views.generic.edit import FormMixin
from django.db.models import Q
from django.utils.translation import ugettext as _
from django.utils.safestring import mark_safe

from .models import ResidentalComplex, NewApartment
from .forms import SearchForm

from company.models import BankPartner


REGEX_FOR_ANY_TEXT_FIELD = re.compile(r'[^\w]', re.I | re.U)


class ResidentalComplexList(FormMixin, ListView):
    form_class = SearchForm
    model = ResidentalComplex
    context_object_name = 'residental_complexes'
    template_name = 'new_buildings/residental_complex_list.html'
    queryset = model.objects.filter(is_active=True).prefetch_related(
        'type_of_complex')

    def aparmentByAnyTextIContains(self, fieldname=None, model_fields=[]):
        # in developing. Think about using Manager
        # https://stackoverflow.com/questions/2276768/django-query-filtering-from-model-method
        if type(model_fields) not in (list, tuple):
            raise Http404('model fields must be list or tuple')
        combined_query = Q()
        values = REGEX_FOR_ANY_TEXT_FIELD.split(
            self.form.cleaned_data[fieldname])
        for model_field in model_fields:
            for value in values:
                combined_query = combined_query | Q(
                    **{'%s__icontains' % model_field: value})
        if combined_query:
            new_filter = self.apartment_list.filter(combined_query)
            if new_filter:
                self.apartment_list = new_filter

    def filterApartmentCheckbox(self, fieldname=None):
        combined_query = Q()
        for value in self.form.cleaned_data[fieldname]:
            if value == '0':
                combined_query = combined_query | Q(
                    **{'%s__exact' % fieldname: "B"})
            elif value < '4':
                combined_query = combined_query | Q(
                    **{'%s__exact' % fieldname: value})
            else:
                combined_query = combined_query | Q(
                    **{'%s__gte' % fieldname: value})
        if combined_query:
            self.apartment_list = self.apartment_list.filter(combined_query)

    def filterApartment(
        self,
        fieldname=None,
        filter_name=None,
        filter_condition_by_value=None
    ):
        if self.form.is_valid() and fieldname and filter_name:
            data = self.form.cleaned_data[fieldname]
            if data:
                self.apartment_list = self.apartment_list.filter(
                    **{filter_name: data})

    def get(self, request, *args, **kwargs):
        # From ProcessFormMixin
        form_class = self.get_form_class()
        data = getattr(request, request.method)

        self.form = form_class(data)

        # From BaseListView
        self.apartment_list = NewApartment.objects.filter(
            is_active=True,
            buildings__is_active=True)
        self.object_list = self.get_queryset()

        if data and self.form.is_valid():
            # Standart filters for fields
            self.filterApartment(fieldname='price_from',
                                 filter_name='price__gte')
            self.filterApartment(fieldname='price_to',
                                 filter_name='price__lte')
            self.filterApartment(fieldname='area_from',
                                 filter_name='total_area__gte')
            self.filterApartment(fieldname='area_to',
                                 filter_name='total_area__lte')

            # Special filter for checbox
            self.filterApartmentCheckbox(fieldname='rooms')

            self.aparmentByAnyTextIContains(
                fieldname='any_text',
                model_fields=[
                    'residental_complex__neighbourhood__name',
                    'residental_complex__name',
                    'buildings__street__name',
                ],
            )

            # For filters by date of cunstruction
            settlement_before = self.form.cleaned_data['settlement_before']

            if settlement_before:
                self.apartment_list = self.apartment_list.filter(
                    date_of_construction__lte=settlement_before,
                )

            self.object_list = self.object_list.filter(
                newapartment__in=self.apartment_list,
            ).distinct()

        allow_empty = self.get_allow_empty()
        if not allow_empty and len(self.object_list) == 0:
            raise Http404(
                _(u"Empty list and '%(class_name)s.allow_empty' is False.") %
                {'class_name': self.__class__.__name__}
            )
        empty_list_flag = False
        if not self.object_list:
            self.object_list = self.get_queryset()
            empty_list_flag = True

        context = self.get_context_data(
            object_list=self.object_list,
            form=self.form,
            empty_list_flag=empty_list_flag
        )
        return self.render_to_response(context)

    def post(self, request, *args, **kwargs):
        return self.get(request, *args, **kwargs)


class ResidentalComplexDetail(DetailView):
    model = ResidentalComplex
    context_object_name = 'residental_complex'
    template_name = 'new_buildings/residental_complex_detail.html'
    queryset = model.objects.filter(is_active=True)

    def get_context_data(self, *args, **kwargs):
        context = super().get_context_data(*args, **kwargs)
        lats = []
        lngs = []
        building_types = []
        for buildings in context[self.context_object_name].get_new_buildings():
            lat, lng = buildings.coordinates_as_list
            if lat and lng:
                lats.append(lat)
                lngs.append(lng)
            building_type = buildings.get_building_type_display().lower()
            if building_type not in building_types:
                building_types.append(building_type)

        if lats and lngs:
            lats = [float(i) for i in lats]
            lngs = [float(i) for i in lngs]
            context['yandex_grid_center_json'] = mark_safe(
                json.dumps([median(lats), median(lngs)]))

        if building_types:
            context['building_types'] = '/'.join(building_types)
        else:
            context['building_types'] = '-'

        context['banks'] = BankPartner.objects.all()
        return context


class NewApartmentsFeed(ListView):
    model = NewApartment
    context_object_name = 'apartments'
    template_name = 'new_buildings/feeds/new-apartments-yandex.xml'
    content_type = "application/xhtml+xml"
    queryset = model.objects.prefetch_related('buildings')\
        .prefetch_related('buildings__residental_complex')\
        .filter(
            is_active=True,
            buildings__is_active=True,
            residental_complex__is_active=True,
    )
