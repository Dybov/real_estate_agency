import re

from django.shortcuts import render, render_to_response
from django.views.generic import ListView, DetailView
from django.views.generic.edit import FormMixin
from django.db.models import Q
from django.utils.translation import ugettext as _


from .models import ResidentalComplex, NewBuilding, NewApartment
from .forms import SearchForm

REGEX_FOR_ANY_TEXT_FIELD = re.compile(r'[^\w]', re.I|re.U)

class ResidentalComplexList(FormMixin, ListView):
    form_class = SearchForm
    model = ResidentalComplex
    context_object_name = 'residental_complexes'
    template_name = 'new_buildings/residental_complex_list.html'
    queryset = model.objects.filter(is_active=True)


    def filterAparmentByAnyText(self, fieldname=None, model_fields=[]):
        # in developing. Think anout using Manager
        # https://stackoverflow.com/questions/2276768/django-query-filtering-from-model-method
        if type(model_fields) not in (list, tuple):
            raise Exception('model fields must be list or tuple')
        combined_query = Q()
        values = REGEX_FOR_ANY_TEXT_FIELD.split(self.form.cleaned_data[fieldname])
        for model_field in model_fields:
            for value in values:
                combined_query = combined_query | Q(**{'%s__icontains' % model_field:value})
        if combined_query:
            self.apartment_list = self.apartment_list.filter(combined_query)

    def filterApartmentCheckbox(self, fieldname=None):
        combined_query = Q() 
        for value in self.form.cleaned_data[fieldname]:
            if value=='0':
                combined_query = combined_query | Q(**{'%s__exact' % fieldname:"B"})
            elif value<'4':
                combined_query = combined_query | Q(**{'%s__exact' % fieldname:value})
            else:
                combined_query = combined_query | Q(**{'%s__gte' % fieldname:value})
        if combined_query:
            self.apartment_list = self.apartment_list.filter(combined_query)
        

    def filterApartment(self, fieldname=None, filter_name=None, filter_condition_by_value=None):
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
        self.apartment_list = NewApartment.objects.all()
        self.object_list = self.get_queryset()

        if data and self.form.is_valid():
            self.filterApartment(fieldname='price_from',
                                 filter_name='price__gte')
            self.filterApartment(fieldname='price_to',
                                 filter_name='price__lte')
            self.filterApartment(fieldname='area_from',
                                 filter_name='total_area__gte')
            self.filterApartment(fieldname='area_to',
                                 filter_name='total_area__lte')
            self.filterApartmentCheckbox(fieldname='rooms')
            # self.filterAparmentByAnyText(fieldname='any_text', 
            #                              model_fields=['get_neighbourhood'],
            #                              )
            settlement_before = self.form.cleaned_data['settlement_before']

            building_id_list = [
                x.get('building') for x in self.apartment_list.values('building').distinct()]
            buildings = NewBuilding.objects.filter(id__in=building_id_list)
            if settlement_before:
                buildings = buildings.filter(
                    date_of_construction__lte=settlement_before)
            residental_complexes_id_list = [x.get(
                'residental_complex') for x in buildings.values('residental_complex').distinct()]
            self.object_list = self.object_list.filter(
                id__in=residental_complexes_id_list)

        allow_empty = self.get_allow_empty()
        if not allow_empty and len(self.object_list) == 0:
            raise Http404(_(u"Empty list and '%(class_name)s.allow_empty' is False.")
                          % {'class_name': self.__class__.__name__})

        context = self.get_context_data(
            object_list=self.object_list, form=self.form)
        return self.render_to_response(context)

    def post(self, request, *args, **kwargs):
        return self.get(request, *args, **kwargs)


class ResidentalComplexDetail(DetailView):
    model = ResidentalComplex
    context_object_name = 'residental_complex'
    template_name = 'new_buildings/residental_complex_detail.html'
