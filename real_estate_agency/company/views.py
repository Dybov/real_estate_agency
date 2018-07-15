from django.shortcuts import render

from .models import Award


def about(request):
    return render(request,
                  'company/about_company.html',
                  {'awards': Award.objects.all()}
                  )
