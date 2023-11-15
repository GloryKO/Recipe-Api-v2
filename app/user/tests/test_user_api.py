"""Test User API"""

from django.test import TestCase
from django.contrib.auth import get_user_model
from django.urls import reverse

from rest_framework.test import APIClient
from rest_framework import status

#endpoint url to send data 

CREATE_USER_URL = reverse('user:create')

#method to create user for testing

def create_user(**params):
    return get_user_model().objects.create_user(**params)

class PublicUserApiTest(TestCase):
    """test the public feature of the user API e.g register"""
    def setUp(self):
        self.client =APIClient()


    def test_create_user_successful(self):
        payload={
            'email':'test@example.com','password':'pass123','name':'test name'
        }
        res = self.client.post(CREATE_USER_URL,payload)
        self.assertEqual(res.status_code,status.HTTP_201_CREATED)
        user = get_user_model().objects.get(email=payload['email'])
        self.assertTrue(user.check_password(payload['password']))
        self.assertNotIn('password',res.data)
    
    def test_user_with_email_exists_error(self):
        payload= {'email':'test@example.com','password':'testpass123','name':'test name'}
        create_user(**payload)
        res = self.client.post(CREATE_USER_URL,payload)
        self.assertEqual(res.status_code,status.HTTP_400_BAD_REQUEST)
    
    def test_password_too_short_error(self):
        payload = {'email':'test@example.com','password':'pw','name':''}
        res = self.client.post(CREATE_USER_URL,payload)
        self.assertEqual(res.status_code,status.HTTP_400_BAD_REQUEST)
        user_exists = get_user_model().objects.filter(email=payload['email'])
        self.assertFalse(user_exists) #checks that the user does not exist in the db