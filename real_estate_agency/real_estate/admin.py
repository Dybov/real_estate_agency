from django.contrib import admin
from .models import ResidentalComplex, Apartment, Address

from django.utils.translation import ugettext as _

class ResidentalComplexAdmin(admin.ModelAdmin):
	list_display =  ('name', 'active','link_to_address')
	list_editable = ('active',)

class AddressAdmin(admin.ModelAdmin):
	list_display =  ('__str__','link_to_residentalcomplex')

class ApartmentAdmin(admin.ModelAdmin):
	list_display =  ('apartment_number','rooms', 'address','link_to_residentalcomplex')

admin.site.register(ResidentalComplex, ResidentalComplexAdmin)
admin.site.register(Address, AddressAdmin)
admin.site.register(Apartment, ApartmentAdmin)