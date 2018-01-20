from django.test import TestCase

from address.models import NeighbourhoodModel

from .models import *

def create_neighbourhood():
    _objects = NeighbourhoodModel.objects.all()
    if not _objects:
        return NeighbourhoodModel.objects.create(name='МЫС')
    return _objects[0]

def create_builder():
    _objects = Builder.objects.all()
    if not _objects:
        return Builder.objects.create(name='Снегири')
    return _objects[0]

def create_type_of_complex():
    _objects = TypeOfComplex.objects.all()
    if not _objects:
        return TypeOfComplex.objects.create(name='Жилой комплекс')
    return _objects[0]

def create_RC():
    return ResidentalComplex.objects.create(type_of_complex=create_type_of_complex(),
                                            name='super',
                                            description='asd',
                                            builder=create_builder(),
                                            is_active=True,
                                            neighbourhood=create_neighbourhood(),
                                            )

def create_apartment(rc, use_rc_builing=True):
    NewApartment.objects.create(
        layout=get_image_file(),
        total_area=38,
        price=10000,
        building=rc.new_builings,
        )

class ResidentalComplexMethodTests(TestCase):
    def test_get_lowest_price(self):
        """
        test_get_lowest_price() should minimal price of apartments which
        can be shown at site (is_active=True) and which are presented
        in appropriate buildings (have m2m link and is_active=True for building)
        """
        obj = create_RC()
        rc = obj.get_lowest_price()
        self.assertIsNone(rc)
        # create_apartment(obj)
        # rc = obj.get_lowest_price()
        # self.assertEqual(10000)


    def test_get_highest_price(self):
        pass



'''
class QuestionMethodTests(TestCase):

    def test_was_published_recently_with_future_question(self):
        """
        was_published_recently() should return False for questions whose
        pub_date is in the future.
        """
        time = timezone.now() + datetime.timedelta(days=30)
        future_question = Question(pub_date=time)
        self.assertEqual(future_question.was_published_recently(), False)
'''