from django.shortcuts import render

from new_buildings.models import ResidentalComplex
from new_buildings.forms import NewBuildingsSearchForm
from feedback.models import Feedback


def corporation_benefit_plan(request):
    return render(request, 'corporation_benefit_plan.html')


def index(request):
    # Only 2 requests to DB
    feedbacks = Feedback.objects.all(
    )[:4].select_related().prefetch_related('social_media_links')
    # Only 2 requests to DB
    residental_complexes = ResidentalComplex.objects.filter(
        is_popular=True).prefetch_related('type_of_complex')
    context = {
        'feedbacks': feedbacks,
        'form': NewBuildingsSearchForm,
        'residental_complexes': residental_complexes,
    }
    return render(request,
                  'index.html',
                  context,
                  )


def privacy_policy(request):
    return render(request, 'privacy_policy.html')


def thanks(request):
    return render(request, 'thanks.html')
