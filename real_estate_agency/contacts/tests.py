from django.test import TestCase

from .views import phone_stringify


class PhoneStringifyTest(TestCase):
    def test_mobile_number(self):
        number = '+79993332525'
        stringified = phone_stringify(number)
        self.assertEqual(stringified, '+7 (999) 333-25-25')

    def test_city_number(self):
        number = '+73452332525'
        stringified = phone_stringify(number)
        self.assertEqual(stringified, '+7 (3452) 33-25-25')

    def test_country_code(self):
        number = '83452332525'
        stringified = phone_stringify(number)
        self.assertEqual(stringified, '8 (3452) 33-25-25')
