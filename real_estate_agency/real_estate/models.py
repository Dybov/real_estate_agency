from django.db import models
from django.utils.translation import ugettext as _
from .utils import admin_change_model
from django.template.defaultfilters import escape


class ResidentalComplex(models.Model):
	"""docstring for ResidentalComplex
	It includes a lot of apartments."""
	name = 	models.CharField(verbose_name=_('название'), max_length=127)
	active = models.BooleanField(verbose_name=_('отображать в новостройках'), default=False)
	
	def link_to_address(self):
		return admin_change_model(self.address)

	link_to_address.allow_tags = True
	link_to_address.short_description = _("адрес" )

	def __str__(self):
		return self.name

	class Meta:
		verbose_name = _('жилой комплекс')
		verbose_name_plural  = _('жилые комплексы')

class Apartment(models.Model):
	BACHELOR = 'B'
	ONEROOM  = '1'
	TWOROOM  = '2'
	THREEROOM  = '3'
	FOURROOM = '4'
	ROOMS_CHOICES = (
			(BACHELOR, _('студия')),
			(BACHELOR, _('1')),
			(BACHELOR, _('2')),
			(BACHELOR, _('3')),
			(BACHELOR, _('4')),
		)

	apartment_number = models.IntegerField(verbose_name=_('квартира'))
	rooms = models.CharField(max_length=1,
							 choices=ROOMS_CHOICES,
							 default=ONEROOM,
							 verbose_name=_('количество комнат'))
	floor   = models.PositiveIntegerField(verbose_name=_('этаж'), default=1)
	address = models.ForeignKey('Address', 
								on_delete=models.CASCADE, 
								null=True,
								related_name='apartment',
								verbose_name=_('адрес'))

	def __str__(self):
		return _("%s кв. %s") % (self.address, self.apartment_number)

	def link_to_residentalcomplex(self):
		return self.address.link_to_residentalcomplex()
	link_to_residentalcomplex.allow_tags = True
	link_to_residentalcomplex.short_description = _("ЖК")

	class Meta:
		verbose_name = _('квартира')
		verbose_name_plural  = _('квартиры')



class Address(models.Model):
	residental_complex = models.OneToOneField('ResidentalComplex', 
											on_delete=models.CASCADE,
											related_name='address',
											verbose_name=_('ЖК'),
											null=True,
											blank=True)
	street = models.CharField(verbose_name=_('улица'), max_length=127)
	building = models.IntegerField(verbose_name=_('дом'))
	building_block = models.IntegerField(verbose_name=_('корпус'), 
										null=True,
										blank=True)
	zip_code = models.CharField(verbose_name=_('почтовый индекс'), max_length=127, null=True, blank=True)
	def __str__(self):
		return self.full_address
	
	@property
	def full_address(self):
		address = _('Ул. %s, д. %s.') % (self.street, self.building)
		if self.building_block:
			address+=_('/%s') % (self.building_block)
		return address

	class Meta:
		verbose_name = _('адрес')
		verbose_name_plural  = _('адреса')

	def link_to_residentalcomplex(self):
		return admin_change_model(self.residental_complex)

	link_to_residentalcomplex.allow_tags = True
	link_to_residentalcomplex.short_description = _("ЖК" )