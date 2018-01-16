from django.shortcuts import render
from django.template import RequestContext

from new_buildings.models import Builder, ResidentalComplex, NewApartment


def about_company_in_digits_context_processor(request):
    """A context processor that provides counting objects for statitistic"""
    # create request for RC and all related flats in only 3 queries
    residental_complex_objects = ResidentalComplex.objects.filter(is_active=True).prefetch_related(
        'newbuilding_set').prefetch_related('newapartment_set')
    residental_complexes_for_output = residental_complex_objects.filter(
        is_popular=True
    )

    # count number of apartments, using db field of RC (implements in
    # count_flats method)
    number_of_apartments = 0
    for rc in residental_complex_objects:
        number_of_apartments += rc.count_flats()

    return {
        'number_of_builders': Builder.objects.count(),
        'number_of_residental_complexes': residental_complex_objects.count(),
        'number_of_apartments': number_of_apartments,
        'residental_complexes': residental_complexes_for_output,
    }

def about(request):
    context = {}
    context.update(about_company_in_digits_context_processor(request))
    return render(request, 
                  'company/about_company.html',
                  context,
                  )
