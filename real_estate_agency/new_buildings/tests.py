import datetime

from django.core.files import File
from django.test import TestCase, tag

from .models import *
from .helpers import get_quarter_verbose

from address.models import StreetModel, NeighbourhoodModel


import mock


NULL_PRICE = ''
NULL_DATE_OF_CONSTRUCTION = ''


file_mock = mock.MagicMock(spec=File, name='FileMock')
file_mock.name = 'test1.jpg'


def get_image_file():
    return file_mock


def create_neighbourhood(name='neighbourhood'):
    _objects = NeighbourhoodModel.objects.filter(name=name)
    if not _objects:
        return NeighbourhoodModel.objects.create(name=name)
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


def create_RC(name='RC', description='smthng', is_active=True, **kwargs):
    """ Creates Residental Complex.
    Adds builder, neighbourhood and type_of_complex objs automatically
    if its not provides"""
    builder = kwargs.pop('builder', create_builder())
    neighbourhood = kwargs.pop('neighbourhood', create_neighbourhood())
    type_of_complex = kwargs.pop('type_of_complex', create_type_of_complex())

    return ResidentalComplex.objects.create(name=name,
                                            description=description,
                                            is_active=is_active,
                                            builder=builder,
                                            neighbourhood=neighbourhood,
                                            type_of_complex=type_of_complex,
                                            **kwargs
                                            )


def create_apartment(rc, price, total_area=38, **kwargs):
    return NewApartment.objects.create(
        residental_complex=rc,
        total_area=total_area,
        price=price,
        layout=get_image_file(),
        **kwargs
    )


def create_building(rc, building_number=1, **kwargs):
    date_of_start_of_construction = kwargs.pop(
        'date_of_start_of_construction', datetime.datetime.now())
    street = kwargs.pop('street', create_street())

    return NewBuilding.objects.create(
        residental_complex=rc,
        date_of_start_of_construction=date_of_start_of_construction,
        street=street,
        building=building_number,
        **kwargs
    )


def create_street():
    _objects = StreetModel.objects.all()
    if not _objects:
        return StreetModel.objects.create(
            name='Street'
        )
    return _objects[0]


def buildings_factory(rc, buildings_amount, no_active_buildings_amount=0):
    """ Create set of NewBuilding objs"""
    buildings = []
    for i in range(buildings_amount):
        buildings.append(create_building(
                rc,
                name=str(i),
                building_number=i,
                date_of_construction=datetime.datetime.now(),
            )
        )
    for i in range(buildings_amount, 
                   buildings_amount+no_active_buildings_amount):
        date = datetime.datetime.now()-datetime.timedelta(days=180)
        buildings.append(create_building(
                rc,
                name=str(i),
                building_number=i,
                date_of_construction=date,
                is_active=False,
            )
        )
    return buildings


class RCBaseTest(TestCase):
    def setUp(self):
        self.RC = create_RC()


@tag('get_lowest_price')
class ResidentalComplexLowestPricesMethodTests(RCBaseTest):
    def test_get_lowest_price_without_apartment(self):
        """
        test_get_lowest_price() should minimal price of apartments which
        can be shown at site (is_active=True) and which are presented
        in appropriate buildings (have m2m link and is_active=True for building)
        """

        price = self.RC.get_lowest_price()
        self.assertEqual(price, NULL_PRICE)

    def test_get_lowest_price_with_apartment_with_building(self):
        apartment_price = 111

        building = create_building(self.RC)
        apartment = create_apartment(self.RC, apartment_price)
        apartment.buildings = [building]
        price = self.RC.get_lowest_price()
        self.assertEqual(price, apartment_price)

    def test_get_lowest_price_with_apartment_without_building(self):

        apartment = create_apartment(self.RC, 222)
        price = self.RC.get_lowest_price()
        self.assertEqual(price, NULL_PRICE)

    def test_get_lowest_price_with_apartment_with_building_noactive(self):
        apartment_price = 333

        building = create_building(self.RC, is_active=False)
        apartment = create_apartment(self.RC, apartment_price)
        apartment.buildings = [building]
        price = self.RC.get_lowest_price()
        self.assertEqual(price, NULL_PRICE)

    def test_get_lowest_price_with_apartment_noactive_with_building(self):
        apartment_price = 444

        building = create_building(self.RC)
        apartment = create_apartment(self.RC, apartment_price, is_active=False)
        apartment.buildings = [building]
        price = self.RC.get_lowest_price()
        self.assertEqual(price, NULL_PRICE)

    @tag('slow')
    def test_get_lowest_price_with_few_apartments_in_one_builing(self):
        lowest_price = 555
        prices = [lowest_price, lowest_price+5, lowest_price+10]

        building = create_building(self.RC)
        for apartment_price in prices:
            apartment = create_apartment(self.RC, apartment_price)
            apartment.buildings = [building]
        price = self.RC.get_lowest_price()
        self.assertEqual(price, lowest_price)

    @tag('slow')
    def test_get_lowest_price_with_mixed_apartments_and_buildings(self):
        [
            building1,
            building2,
            building3,
            building_no_active
        ] = buildings_factory(self.RC, 3, 1)
        apartment1 = create_apartment(self.RC, 666)
        apartment1.buildings = [building1, building3, building_no_active]

        apartment2 = create_apartment(self.RC, 667)
        apartment2.buildings = [building2, building_no_active]

        apartment3 = create_apartment(self.RC, 668)
        apartment3.buildings = [building1,
                                building2,
                                building3,
                                building_no_active]

        apartment_no_active = create_apartment(self.RC, 660, is_active=False)
        apartment_no_active.buildings = [building1,
                                         building2,
                                         building3,
                                         building_no_active]

        apartment_with_no_active_building = create_apartment(self.RC, 650)
        apartment_with_no_active_building.buildings = [building_no_active]

        price = self.RC.get_lowest_price()
        self.assertEqual(price, 666)


@tag('get_date_of_construction')
class ResidentalComplexNearestDatesMethodTests(RCBaseTest):
    def test_get_date_of_construction_without_buildings(self):
        date_of_construction = self.RC.get_date_of_construction()
        self.assertEqual(date_of_construction, NULL_DATE_OF_CONSTRUCTION)

    def test_get_date_of_construction_with_building(self):
        date_of_construction_of_building = datetime.datetime.now()
        building = create_building(
            self.RC,
            date_of_construction=date_of_construction_of_building
        )

        date_of_construction = self.RC.get_date_of_construction()
        self.assertEqual(
            date_of_construction,
            get_quarter_verbose(date_of_construction_of_building)
        )

    def test_get_date_of_construction_with_building_no_active(self):
        building = create_building(
            self.RC,
            date_of_construction=datetime.datetime.now(),
            is_active=False,
        )

        date_of_construction = self.RC.get_date_of_construction()
        self.assertEqual(date_of_construction, NULL_DATE_OF_CONSTRUCTION)

    @tag('slow')
    def test_get_date_of_construction_with_mixed_buildings(self):
        [
            building1,
            building2,
            building3,
            building_no_active1,
            building_no_active2,
        ] = buildings_factory(self.RC, 3, 2)

        nearest_date = building1.date_of_construction
        date_of_construction = self.RC.get_date_of_construction()
        self.assertEqual(
            date_of_construction,
            get_quarter_verbose(nearest_date),
        )

@tag('slow', 'view')
class ResidentalComplexListViewSearchFilterTests(TestCase):
    def RCWithBuildingWithApartmentFactory(
            self, rc_numbers, rc_name_prefix='RC', 
            rc_kwargs={}, building_kwargs={}, apartment_kwargs={}):
        all_rc = []
        for rc_number in range(rc_numbers):
            rc = create_RC(
                name = rc_name_prefix+" %s" % rc_number,
                **rc_kwargs
                )
            all_rc.append(rc)
            building = create_building(rc, **building_kwargs)
            price = apartment_kwargs.pop('price', 190000)
            apartment = create_apartment(rc, price, **apartment_kwargs)
            apartment.buildings = [building]
        return all_rc

    def test_search_by_any_text_neigbourhood(self):
        target_neigbourhood = create_neighbourhood('МЫС')
        non_target_neigbourhood = create_neighbourhood('Дом Обороны')
        number_of_rc_with_target_neigbourhood = 6

        target_rcs = self.RCWithBuildingWithApartmentFactory(
            number_of_rc_with_target_neigbourhood,
            "Target RC",
            rc_kwargs={'neighbourhood':target_neigbourhood}
        )

        non_target_rcs = self.RCWithBuildingWithApartmentFactory(
            10,
            "Non-Target RC",
            rc_kwargs={'neighbourhood':non_target_neigbourhood}
        )+self.RCWithBuildingWithApartmentFactory(
            10,
            "no-active RC with appropriate neigbourhood",
            rc_kwargs={
                'is_active':False,
                'neighbourhood':target_neigbourhood,
            }
        )

        resp = self.client.get(
            reverse('new_buildings:residental-complex-list'),
            {'any_text':target_neigbourhood.name}
        )
        self.assertEqual(resp.status_code, 200)
        self.assertTrue(len(resp.context['residental_complexes']) == number_of_rc_with_target_neigbourhood)