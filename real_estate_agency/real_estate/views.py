from django.shortcuts import render, HttpResponse


def index(request):
    return render(request, 'real_estate/index.html')

def privacy_policy(request):
    return render(request, 'real_estate/privacy_policy.html')