from django.shortcuts import render,render_to_response
from django.template import RequestContext

from new_buildings.models import Builder, ResidentalComplex, NewApartment
from new_buildings.forms import SearchForm
from feedback.models import Feedback
from company.views import about_company_in_digits_context_processor

def corporation_benefit_plan(request):
    return render(request, 'corporation_benefit_plan.html')


def index(request):
    feedbacks = Feedback.objects.all()[:4]
    context = {
        'feedbacks': feedbacks,
        'form': SearchForm,
    }
    context.update(about_company_in_digits_context_processor(request))
    return render(request,
                  'index.html',
                  context,
                  )


def privacy_policy(request):
    return render(request, 'privacy_policy.html')


def thanks(request):
    return render(request, 'thanks.html')