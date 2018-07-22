import re

from django.db.models import Q
from django.shortcuts import Http404

REGEX_FOR_ANY_TEXT_FIELD = re.compile(r'[^\w]', re.I | re.U)


class ApartmentFilterMixin(object):
    """ApartmentFilterMixin is an mixin for searching in CBV
    it filter self.apartment_list using data from self.form
    """

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
                    **{'%s__gte' % fieldname: value,
                       # It needs for queries without 'B'
                       # 'B' is greater than 'A'
                       '%s__lt' % fieldname: 'A'}
                )
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

    def filterTotalArea(self):
        self.filterApartment(fieldname='area_from',
                             filter_name='total_area__gte')
        self.filterApartment(fieldname='area_to',
                             filter_name='total_area__lte')

    def filterPrice(self):
        self.filterApartment(fieldname='price_from',
                             filter_name='price__gte')
        self.filterApartment(fieldname='price_to',
                             filter_name='price__lte')

    def filterRooms(self):
        self.filterApartmentCheckbox(fieldname='rooms')

    def standartApartmentFilter(self):
        self.filterTotalArea()
        self.filterPrice()
        self.filterRooms()
