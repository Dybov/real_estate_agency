from django.test import TestCase
from django.contrib.auth import get_user_model

from .models import RealEstateUser


class RealEstateUserTest(TestCase):
    def setUp(self):
        self.user = get_user_model().objects.create_user(
            'testuser', 'test@mail.test', 'testpass',
        )

    def test_settings(self):
        self.assertIsInstance(self.user, RealEstateUser)

    def test_user_fields(self):
        self.assertEqual(self.user.email, 'test@mail.test')
        self.assertEqual(self.user.username, 'testuser')
        self.assertTrue(self.user.check_password('testpass'))
