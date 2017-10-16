from django.contrib import admin
#from django import forms

from .models import ResidentalComplex, NewBuilding, Builder


class BuildingInline(admin.StackedInline):
    model = NewBuilding
    extra = 1


class ResidentalComplexAdmin(admin.ModelAdmin):
    inlines = [BuildingInline, ]
    list_display = ('name', 'active')
    list_editable = ('active',)

admin.site.register(ResidentalComplex, ResidentalComplexAdmin)
admin.site.register(Builder)
# admin.site.register(NewBuilding)
