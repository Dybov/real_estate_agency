#from django.contrib import admin
from django.contrib.admin import AdminSite
from django.contrib.admin import ModelAdmin
from .models import ResidentalComplex, Apartment, Address

from django.utils.translation import ugettext as _

class MyAdminSite(AdminSite):
    site_header = _('Администрирование DОМУС')
    site_title  = _('DОМУС')

admin = MyAdminSite(name='admin')

# Register your models here.

class ResidentalComplexAdmin(ModelAdmin):
	list_display =  ('name', 'active','link_to_address')
	list_editable = ('active',)

class AddressAdmin(ModelAdmin):
	list_display =  ('__str__','link_to_residentalcomplex',)

class ApartmentAdmin(ModelAdmin):
	list_display =  ('apartment_number','rooms', 'address', )

admin.register(ResidentalComplex, ResidentalComplexAdmin)
admin.register(Address, AddressAdmin)
admin.register(Apartment, ApartmentAdmin)