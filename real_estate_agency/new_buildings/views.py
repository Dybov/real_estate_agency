from django.shortcuts import render
from django.views.generic import ListView, DetailView
from .models import ResidentalComplex, NewBuilding, NewApartment

class ResidentalComplexList(ListView):
    model = ResidentalComplex
    context_object_name = 'residental_complexes'
    template_name = 'new_buildings/residental_complex_list.html'
    queryset = model.objects.filter(is_active=True)

    def post(self, request, *args, **kwargs):

        price_from = request.POST.get('search_price_from')
        price_to = request.POST.get('search_price_to')
        print(price_from,price_to)
        if price_from:
            try:
                price_from = float(price_from)
            except:
                price_from = None
        if price_to:
            try:
                price_to = float(price_to)
            except:
                price_to = None
        if price_from and price_to:
            if price_from > price_to:
                price_from = None
        print(price_from,price_to)
        print('-'*15)
        queryset = NewApartment.objects.all()
        if price_to:
            print(1)
            queryset = queryset.filter(price__lte=price_to)
        if price_from:
            print(1)
            queryset = queryset.filter(price__gte=price_from)
        _complexes = []

        search_area_from = request.POST.get('search_area_from')
        search_area_to = request.POST.get('search_area_to')
        print(search_area_from,search_area_to)
        try:
            if search_area_from:
                search_area_from = float(search_area_from)
            if search_area_to:
                search_area_to = float(search_area_to)
        except:
            search_area_from = None
            search_area_to = None
        if search_area_from and search_area_to:
            if search_area_from > search_area_to:
                search_area_from = None

        if search_area_to:
            queryset = queryset.filter(total_area__lte=search_area_to)
        if search_area_from:
            queryset = queryset.filter(total_area__gte=search_area_from)
        print(queryset)
        for apartment in queryset:
            _complex = apartment.get_residental_complex()
            if _complex not in _complexes:
                _complexes.append(_complex)
        print(_complexes)
        return render(request, self.template_name, {self.context_object_name: _complexes})

class ResidentalComplexDetail(DetailView):
    model = ResidentalComplex
    context_object_name = 'residental_complex'
    template_name = 'new_buildings/residental_complex_detail.html'
    #queryset = model.objects.filter(active=True)