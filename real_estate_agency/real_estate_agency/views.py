from django.shortcuts import render

from new_buildings.models import Builder, ResidentalComplex, NewApartment


def about(request):
    return render(request, 'about.html')


def feedback(request):
    return render(request, 'feedback.html')


def corporation_benefit_plan(request):
    return render(request, 'corporation_benefit_plan.html')


def index(request):
    # create request for RC and all related flats in only 3 queries
    residental_complex_objects = ResidentalComplex.objects.filter(is_active=True).prefetch_related(
        'newbuilding_set').prefetch_related('newbuilding_set__newapartment_set')
    residental_complexes_for_output = residental_complex_objects.filter(
        is_popular=True
    )

    # count number of apartments, using db field of RC (implements in
    # count_flats method)
    number_of_apartments = 0
    for rc in residental_complex_objects:
        number_of_apartments += rc.count_flats()

    context = {
        'number_of_builders': Builder.objects.count(),
        'number_of_residental_complexes': residental_complex_objects.count(),
        'number_of_apartments': number_of_apartments,
        'residental_complexes': residental_complexes_for_output,
    }
    return render(request, 'index.html', context)


def privacy_policy(request):
    return render(request, 'privacy_policy.html')


def thanks(request):
    return render(request, 'thanks.html')