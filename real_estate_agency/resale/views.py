from django.shortcuts import render
from django.shortcuts import get_object_or_404

from .models import ResaleApartment


def index(request):
    context = {'apartments': ResaleApartment.objects.filter(is_active=True),}
    return render(request, 'resale/resale_list.html', context)

def detailed(request, pk):
    context = {'apartment':get_object_or_404(ResaleApartment, pk=pk)}
    return render(request, 'resale/resale_detailed.html', context)
