from django.db.models import Q
from django.test import TestCase, tag
from django.urls import reverse

from new_buildings.tests import create_RC
from real_estate.test_helper import (
    create_street,
    create_neighbourhood,
    create_mock_image_file,
)

from .models import ResaleApartment, TransactionMixin
from .views import ResaleListView

DEFAULT_PRICE = 1200000
DEFAULT_TOTAL_AREA = 45
DEFAULT_ROOMS = 1
DEFAULT_ROOM_BACHELOR_IN_DB = 'B'
STATUS_ACTIVE = TransactionMixin.ACTIVE
STATUS_SOLD_WITH_US = TransactionMixin.SOLD_WITH_US
STATUS_SOLD_WITHOUT_US = TransactionMixin.SOLD_WITHOUT_US


def create_resale_apartment(**kwargs):
    owner_name = kwargs.pop('owner_name', "NAME")
    owner_phone_number = kwargs.pop('owner_phone_number', "+79999999999")
    neighbourhood = kwargs.pop(
        'neighbourhood',
        create_neighbourhood(),
    )
    street = kwargs.pop(
        'street',
        create_street()
    )
    total_area = kwargs.pop('total_area', DEFAULT_TOTAL_AREA)
    building = kwargs.pop('building', 777)
    price = kwargs.pop('price', DEFAULT_PRICE)
    agency_price = kwargs.pop('agency_price', price)
    rooms = kwargs.pop('rooms', DEFAULT_ROOMS)

    return ResaleApartment.objects.create(
        agency_price=agency_price,
        price=price,
        owner_name=owner_name,
        owner_phone_number=owner_phone_number,
        neighbourhood=neighbourhood,
        street=street,
        building=building,
        total_area=total_area,
        layout=create_mock_image_file(),
        rooms=rooms,
        **kwargs
    )


class ResaleApartmentViewTest(TestCase):
    """ResaleApartmentViewTest is class for testing
    resale.view.ResaleListView and its filtering
    """
    def setUp(self):
        self.apartment = create_resale_apartment()
        self.view_class = ResaleListView
        self.object_list_name = ResaleListView.context_object_name

    def get_default_queryset(self):
        # it is not self.view_class.queryset for purpose
        # self.view_class.queryset can be broken to
        return ResaleApartment.objects.filter(
            is_active=True,
            status=STATUS_ACTIVE,
        )

    def get_resale_list(self, uri=None, get_params={}):
        if not uri:
            uri = reverse('resale:index')
        response = self.client.get(uri, get_params)
        return response

    def count_resale_objects_from_request(self, get_params={}):
        response = self.get_resale_list(get_params=get_params)
        return len(response.context.get(self.object_list_name))

    def assertResponseObjectListAppropriate(
        self,
        response,
        queryset_for_comparison,
        amount_in,
        must_in=[],
        must_out=[],
    ):
        self.assertEqual(response.status_code, 200)
        response_q = response.context.get(self.object_list_name)

        count_from_response = len(response_q)
        self.assertEqual(count_from_response, amount_in)

        for obj_in in must_in:
            self.assertTrue(obj_in in response_q)

        for obj_out in must_out:
            self.assertFalse(obj_out in response_q)

        # don't use self.assertQuerysetEqual beacause it breaks in sqlite
        self.assertListEqual(
            list(response_q),
            list(queryset_for_comparison),
        )

    def test_content_has_objects(self):
        response = self.get_resale_list()
        self.assertTrue('object_list' in response.context)
        self.assertTrue(self.object_list_name in response.context)
        object_list = list(response.context.get('object_list'))
        named_object_list = list(response.context.get(self.object_list_name))
        self.assertListEqual(object_list, named_object_list)

    @tag('basic')
    def test_apartment_list(self):
        create_resale_apartment()
        create_resale_apartment()

        count = self.count_resale_objects_from_request()
        self.assertEqual(count, 3)

    @tag('active-objects')
    def test_apartment_list_active_false(self):
        create_resale_apartment()
        create_resale_apartment(is_active=False)
        create_resale_apartment(is_active=False)

        count = self.count_resale_objects_from_request()
        self.assertEqual(count, 2)

    @tag('active-objects')
    def test_apartment_list_status_no_active(self):
        create_resale_apartment()
        create_resale_apartment()
        create_resale_apartment(status=STATUS_SOLD_WITHOUT_US)
        create_resale_apartment(status=STATUS_SOLD_WITH_US)

        count = self.count_resale_objects_from_request()
        self.assertEqual(count, 3)

    @tag('active-objects')
    def test_apartment_list_active_false_and_status_no_active(self):
        create_resale_apartment()
        create_resale_apartment(is_active=False)
        create_resale_apartment(status=STATUS_SOLD_WITHOUT_US)
        create_resale_apartment(status=STATUS_SOLD_WITH_US)
        create_resale_apartment(
            status=STATUS_SOLD_WITH_US,
            is_active=False
        )

        count = self.count_resale_objects_from_request()
        self.assertEqual(count, 2)

    @tag('price')
    def test_price_from(self):
        price_from = DEFAULT_PRICE - 30000
        price_out = price_from - 1
        obj_in = create_resale_apartment(price=price_from)
        obj_out = create_resale_apartment(price=price_out)

        q = self.get_default_queryset().filter(price__gte=price_from)

        response = self.get_resale_list(get_params={'price_from': price_from})
        self.assertResponseObjectListAppropriate(
            response, queryset_for_comparison=q, amount_in=2,
            must_in=[self.apartment, obj_in],
            must_out=[obj_out, ]
        )

    @tag('price')
    def test_price_from_with_active_false(self):
        price_from = DEFAULT_PRICE - 30000
        obj_out1 = create_resale_apartment(
            price=price_from,
            is_active=False
        )
        obj_out2 = create_resale_apartment(
            price=price_from,
            status=STATUS_SOLD_WITH_US,
        )
        obj_out3 = create_resale_apartment(
            price=price_from,
            is_active=False,
            status=STATUS_SOLD_WITH_US,
        )
        obj_in = create_resale_apartment(
            price=price_from + 1,
        )

        q = self.get_default_queryset().filter(price__gte=price_from)

        response = self.get_resale_list(get_params={'price_from': price_from})
        self.assertResponseObjectListAppropriate(
            response, queryset_for_comparison=q, amount_in=2,
            must_in=[self.apartment, obj_in],
            must_out=[obj_out1, obj_out2, obj_out3, ]
        )

    @tag('price')
    def test_price_to(self):
        price_to = DEFAULT_PRICE + 30000
        price_out = price_to + 1
        obj_in = create_resale_apartment(price=price_to)
        obj_out = create_resale_apartment(price=price_out)

        q = self.get_default_queryset().filter(price__lte=price_to)
        response = self.get_resale_list(get_params={'price_to': price_to})
        self.assertResponseObjectListAppropriate(
            response, queryset_for_comparison=q, amount_in=2,
            must_in=[self.apartment, obj_in],
            must_out=[obj_out, ]
        )

    @tag('price')
    def test_price_to_with_active_false(self):
        price_to = DEFAULT_PRICE + 30000
        obj_out1 = create_resale_apartment(
            price=price_to,
            is_active=False
        )
        obj_out2 = create_resale_apartment(
            price=price_to,
            status=STATUS_SOLD_WITH_US,
        )
        obj_out3 = create_resale_apartment(
            price=price_to,
            is_active=False,
            status=STATUS_SOLD_WITH_US,
        )
        obj_in = create_resale_apartment(
            price=price_to - 1,
        )

        q = self.get_default_queryset().filter(price__lte=price_to)

        response = self.get_resale_list(get_params={'price_to': price_to})
        self.assertResponseObjectListAppropriate(
            response, queryset_for_comparison=q, amount_in=2,
            must_in=[self.apartment, obj_in],
            must_out=[obj_out1, obj_out2, obj_out3, ]
        )

    @tag('area')
    def test_area_from(self):
        area_from = DEFAULT_TOTAL_AREA - 5
        area_out = area_from - 1
        obj_in = create_resale_apartment(total_area=area_from)
        obj_out = create_resale_apartment(total_area=area_out)

        q = self.get_default_queryset().filter(total_area__gte=area_from)
        response = self.get_resale_list(get_params={'area_from': area_from})
        self.assertResponseObjectListAppropriate(
            response, queryset_for_comparison=q, amount_in=2,
            must_in=[self.apartment, obj_in],
            must_out=[obj_out, ]
        )

    @tag('area')
    def test_area_from_with_active_false(self):
        area_from = DEFAULT_TOTAL_AREA - 5
        obj_out1 = create_resale_apartment(
            total_area=area_from,
            is_active=False
        )
        obj_out2 = create_resale_apartment(
            total_area=area_from,
            status=STATUS_SOLD_WITH_US,
        )
        obj_out3 = create_resale_apartment(
            total_area=area_from,
            is_active=False,
            status=STATUS_SOLD_WITH_US,
        )
        obj_in1 = create_resale_apartment(
            total_area=area_from,
        )
        obj_in2 = create_resale_apartment(
            total_area=area_from + 7,
        )

        q = self.get_default_queryset().filter(total_area__gte=area_from)

        response = self.get_resale_list(get_params={'area_from': area_from})
        self.assertResponseObjectListAppropriate(
            response, queryset_for_comparison=q, amount_in=3,
            must_in=[self.apartment, obj_in1, obj_in2, ],
            must_out=[obj_out1, obj_out2, obj_out3, ]
        )

    @tag('area')
    def test_area_to(self):
        area_to = DEFAULT_TOTAL_AREA + 5
        area_out = area_to + 1
        obj_in = create_resale_apartment(total_area=area_to)
        obj_out = create_resale_apartment(total_area=area_out)

        q = self.get_default_queryset().filter(total_area__lte=area_to)
        response = self.get_resale_list(get_params={'area_to': area_to})
        self.assertResponseObjectListAppropriate(
            response, queryset_for_comparison=q, amount_in=2,
            must_in=[self.apartment, obj_in],
            must_out=[obj_out, ]
        )

    @tag('area')
    def test_area_to_with_active_false(self):
        area_to = DEFAULT_TOTAL_AREA + 5
        obj_out1 = create_resale_apartment(
            total_area=area_to,
            is_active=False
        )
        obj_out2 = create_resale_apartment(
            total_area=area_to,
            status=STATUS_SOLD_WITH_US,
        )
        obj_out3 = create_resale_apartment(
            total_area=area_to,
            is_active=False,
            status=STATUS_SOLD_WITH_US,
        )
        obj_in1 = create_resale_apartment(
            total_area=area_to,
        )
        obj_in2 = create_resale_apartment(
            total_area=area_to - 2,
        )
        obj_in3 = create_resale_apartment(
            total_area=area_to - 5,
        )

        q = self.get_default_queryset().filter(total_area__lte=area_to)

        response = self.get_resale_list(get_params={'area_to': area_to})
        self.assertResponseObjectListAppropriate(
            response, queryset_for_comparison=q, amount_in=4,
            must_in=[self.apartment, obj_in1, obj_in2, obj_in3, ],
            must_out=[obj_out1, obj_out2, obj_out3, ]
        )

    @tag('rooms')
    def test_rooms(self):
        # B stands for bachelor
        rooms_in = [1, 2, 0]

        # To don't forget about self.apartment with default rooms value
        if DEFAULT_ROOMS not in rooms_in:
            rooms_in.append(DEFAULT_ROOMS)

        # It is necessary because in DB bachelor is 'B', but in request it is 0
        rooms_in_for_direct_query = []
        for room in rooms_in:
            room = DEFAULT_ROOM_BACHELOR_IN_DB if room in (0, '0') else room
            rooms_in_for_direct_query.append(room)

        obj_in1 = create_resale_apartment(rooms=1)
        obj_in2 = create_resale_apartment(rooms=DEFAULT_ROOM_BACHELOR_IN_DB)
        obj_out1 = create_resale_apartment(rooms=3)
        obj_out2 = create_resale_apartment(rooms=4)

        q = self.get_default_queryset().filter(
            rooms__in=rooms_in_for_direct_query
        )
        response = self.get_resale_list(get_params={'rooms': rooms_in})
        self.assertResponseObjectListAppropriate(
            response, queryset_for_comparison=q, amount_in=3,
            must_in=[self.apartment, obj_in1, obj_in2, ],
            must_out=[obj_out1, obj_out2, ]
        )

    @tag('rooms')
    def test_rooms_with_active_false(self):
        # B stands for bachelor
        rooms_in = [3, 4]

        obj_in1 = create_resale_apartment(rooms=4)
        obj_in2 = create_resale_apartment(rooms=3)
        obj_out1 = create_resale_apartment(
            rooms=3,
            is_active=False,
        )
        obj_out2 = create_resale_apartment(
            rooms=4,
            status=STATUS_SOLD_WITH_US,
        )
        obj_out3 = create_resale_apartment(rooms=1)
        obj_out4 = create_resale_apartment(rooms=DEFAULT_ROOM_BACHELOR_IN_DB)

        q = self.get_default_queryset().filter(rooms__in=rooms_in)
        response = self.get_resale_list(get_params={'rooms': rooms_in})
        self.assertResponseObjectListAppropriate(
            response, queryset_for_comparison=q, amount_in=2,
            must_in=[obj_in1, obj_in2],
            must_out=[obj_out1, obj_out2, obj_out3, obj_out4]
        )

    @tag('neighbourhood')
    def test_neighbourhood(self):
        neighbourhood_looking_for = create_neighbourhood('Target')
        other_neighbourhood = create_neighbourhood('Non-target')

        obj_in1 = create_resale_apartment(
            rooms=3,
            neighbourhood=neighbourhood_looking_for
        )
        obj_in2 = create_resale_apartment(
            rooms=4,
            neighbourhood=neighbourhood_looking_for
        )
        obj_out = create_resale_apartment(
            rooms=2,
            neighbourhood=other_neighbourhood
        )

        q = self.get_default_queryset().filter(
            neighbourhood=neighbourhood_looking_for)

        response = self.get_resale_list(
            # Important use neighbourhood_looking_for.pk
            get_params={'neighbourhood': neighbourhood_looking_for.pk})

        self.assertResponseObjectListAppropriate(
            response, queryset_for_comparison=q, amount_in=2,
            must_in=[obj_in1, obj_in2],
            must_out=[obj_out, self.apartment]
        )

    @tag('neighbourhood')
    def test_neighbourhood_active_false(self):
        neighbourhood_looking_for = create_neighbourhood('Target')
        other_neighbourhood = create_neighbourhood('Non-target')

        obj_in = create_resale_apartment(
            rooms=3,
            neighbourhood=neighbourhood_looking_for,
        )
        obj_out1 = create_resale_apartment(
            rooms=4,
            neighbourhood=other_neighbourhood,
        )
        obj_out2 = create_resale_apartment(
            rooms=2,
            neighbourhood=neighbourhood_looking_for,
            is_active=False,
        )
        obj_out3 = create_resale_apartment(
            rooms=1,
            neighbourhood=neighbourhood_looking_for,
            status=STATUS_SOLD_WITHOUT_US,
        )

        q = self.get_default_queryset().filter(
            neighbourhood=neighbourhood_looking_for)

        response = self.get_resale_list(
            get_params={'neighbourhood': neighbourhood_looking_for.pk})

        self.assertResponseObjectListAppropriate(
            response, queryset_for_comparison=q, amount_in=1,
            must_in=[obj_in],
            must_out=[obj_out1, obj_out2, obj_out3, self.apartment]
        )

    @tag('any_text')
    def test_search_by_any_text(self):
        target_part = 'detach'
        neighbourhood_looking_for = create_neighbourhood('Semi' + target_part)
        street_looking_for = create_street(target_part + 'ed')
        rc_looking_for = create_RC(name='RC' + target_part)

        obj_in1 = create_resale_apartment(
            neighbourhood=neighbourhood_looking_for)
        obj_in2 = create_resale_apartment(street=street_looking_for)
        obj_in3 = create_resale_apartment(residental_complex=rc_looking_for)

        obj_out1 = create_resale_apartment(rooms=2)
        obj_out2 = create_resale_apartment(rooms=3)
        obj_out3 = create_resale_apartment(rooms=4)

        q = self.get_default_queryset().filter(
            Q(neighbourhood=neighbourhood_looking_for) |
            Q(street=street_looking_for) |
            Q(residental_complex=rc_looking_for)
        )

        response = self.get_resale_list(get_params={'any_text': target_part})

        self.assertResponseObjectListAppropriate(
            response, queryset_for_comparison=q, amount_in=3,
            must_in=[obj_in1, obj_in2, obj_in3, ],
            must_out=[obj_out1, obj_out2, obj_out3, self.apartment]
        )
