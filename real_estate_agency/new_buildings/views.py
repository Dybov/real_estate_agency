from django.shortcuts import render
from django.views.generic import ListView, DetailView
from .models import ResidentalComplex

class ResidentalComplexList(ListView):
    model = ResidentalComplex
    context_object_name = 'residental_complexes'
    template_name = 'new_buildings/residental_complex_list.html'
    queryset = model.objects.filter(is_active=True)

class ResidentalComplexDetail(DetailView):
    model = ResidentalComplex
    context_object_name = 'residental_complex'
    template_name = 'new_buildings/residental_complex_detail.html'
    #queryset = model.objects.filter(active=True)