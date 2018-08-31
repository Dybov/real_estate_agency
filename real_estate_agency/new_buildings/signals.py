from django.db.models.signals import post_save, m2m_changed
from django.dispatch import receiver
from .models import NewBuilding, NewApartment, ResidentalComplex


@receiver(
    post_save,
    sender=NewBuilding,
    dispatch_uid="save_apartment_after_building_saved"
)
def newbuilding_post_saver(sender, instance, created, **kwargs):
    """Set date of construction to NewApartment and RC objects
    if building changes date_of_construction"""
    related_apartments = NewApartment.objects.filter(buildings=instance)
    if not hasattr(instance, 'residental_complex'):
        return
    residental_complex = instance.residental_complex
    for apartment in related_apartments:
        if apartment._set_date_of_construction():
            apartment.save()
    if residental_complex._set_date_of_construction():
        residental_complex.save()


@receiver(m2m_changed,
          sender=NewApartment.buildings.through,
          dispatch_uid="save_apartment_if_m2m_changed")
def apartment_m2m_changer(sender, instance, action, reverse, **kwargs):
    """ Set date of construction to NewApartment obj
    if it changes building field and these date changed beacuse of that"""
    if not reverse and action == "post_add":
        if instance._set_date_of_construction():
            instance.save()
        if instance.residental_complex._set_lowest_price():
            instance.residental_complex.save()


@receiver(
    post_save,
    sender=ResidentalComplex,
    dispatch_uid="set_prices_to_rc"
)
def residental_complex_price_setter(sender, instance, **kwargs):
    if instance._set_lowest_price():
        instance.save()
