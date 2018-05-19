from django.contrib import admin

from .models import ResaleApartment


@admin.register(ResaleApartment)
class ResaleApartmentAdmin(admin.ModelAdmin):
    pass