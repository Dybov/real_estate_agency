from django.contrib import admin

from .models import NeighbourhoodModel, StreetModel


@admin.register(StreetModel)
class StreetModelAdmin(admin.ModelAdmin):
    pass


admin.site.register(NeighbourhoodModel)
# admin.site.register(StreetModel)
