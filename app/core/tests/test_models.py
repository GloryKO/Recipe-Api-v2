"""Test for models"""

from django.test import TestCase
from django.contrib.auth import get_user_model

class ModelTestCase(TestCase):

    def test_create_user_with_email_success(self):
        email='test@example.com'
        password= 'testpass123'
        user =get_user_model().objects.create(email=email,password=password)
        self.assertEqual(user.email,email)
        self.assertEqual(user.check_password(password))
        