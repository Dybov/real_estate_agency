from django.shortcuts import render


def about(request):
    return render(request, 'about.html')

def mortgage(request):
    return render(request, 'mortgage.html')

def feedback(request):
    return render(request, 'feedback.html')

def corporation_benefit_plan(request):
    return render(request, 'corporation_benefit_plan.html')

def contacts(request):
    return render(request, 'contacts.html')