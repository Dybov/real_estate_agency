from django.shortcuts import render


def about(request):
    return render(request, 'about.html')

def feedback(request):
    return render(request, 'feedback.html')

def corporation_benefit_plan(request):
    return render(request, 'corporation_benefit_plan.html')

def contacts(request):
    return render(request, 'contacts.html')

def index(request):
    return render(request, 'index.html')

def privacy_policy(request):
    return render(request, 'privacy_policy.html')