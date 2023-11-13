"""Test Django Admin Modifications"""

from django.test import TestCase
from django.test import TestCase
from django.contrib.auth import get_user_model
from django.urls import reverse
from django.test import Client

class AdminSiteTests(TestCase):
    "Test for django admin"
    def setUp(self):
        self.client = Client()
        self.admin_user = get_user_model().objects.create_superuser(
            email='admin@example.com',password='testpass123',
        )
        self.client.force_login(self.admin_user)
        self.user = get_user_model().objects.create_user(email='testuser@example.com',password='testpass123',name='test user')
    
    def test_users_list(self):
        url = reverse('admin:core_user_change_list')
        res = self.client.get(url)