from django.shortcuts import render, render_to_response
from django.template import RequestContext

from new_buildings.models import Builder, ResidentalComplex, NewApartment
from new_buildings.forms import SearchForm
from feedback.models import Feedback


def corporation_benefit_plan(request):
    return render(request, 'corporation_benefit_plan.html')


def index(request):
    # Only 4 requests to DB
    feedbacks = Feedback.objects.all()[:4].prefetch_related(
        'bought').prefetch_related(
        'bought__type_of_complex').prefetch_related('social_media_links')
    context = {
        'feedbacks': feedbacks,
        'form': SearchForm,
    }
    return render(request,
                  'index.html',
                  context,
                  )


def privacy_policy(request):
    return render(request, 'privacy_policy.html')


def thanks(request):
    return render(request, 'thanks.html')
