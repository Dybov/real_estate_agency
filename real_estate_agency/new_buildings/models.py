from django.db import models
from django.utils.translation import ugettext as _

from real_estate.models import PropertyImage, Apartment


class NewApartment(Apartment):  # , BaseUniqueModel):
	is_primary = True