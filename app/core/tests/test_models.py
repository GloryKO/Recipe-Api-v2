"""Test for models"""

from django.test import TestCase
from django.contrib.auth import get_user_model
from core import models 
from decimal import Decimal

def create_user(email='user@example.com',password='pass123'):
    return get_user_model().objects.create_user(email,password)

class ModelTestCase(TestCase):
    def test_create_user_with_email_success(self):
        """test create user with email"""
        email='test@example.com'
        password= 'testpass123'
        user =get_user_model().objects.create_user(email=email,password=password)
        self.assertEqual(user.email,email)
        self.assertTrue(user.check_password(password))

    def test_normalize_new_user_email(self):
        """test email is normlaized for users"""
        sample_emails=[
            ['test1@EXAMPLE.com', 'test1@example.com'],
            ['Test2@Example.com', 'Test2@example.com'],
            ['TEST3@EXAMPLE.com', 'TEST3@example.com'],
            ['test4@example.COM', 'test4@example.com'],
        ]
        for email,expected in sample_emails:
            user = get_user_model().objects.create_user(email,'pass123')
            self.assertEqual(user.email,expected)
    
    def test_new_user_without_email_raises_error(self):
        with self.assertRaises(ValueError):
            get_user_model().objects.create_user('','pass123')
    

    def test_create_supr_user(self):
        """Testing creating a superuser"""
        user = get_user_model().objects.create_superuser(
            'test@example.com','testpass123'
        )
        self.assertTrue(user.is_superuser)
        self.assertTrue(user.is_staff)
    
    def test_create_recipe(self):
        user=get_user_model().objects.create_user('test@example.com','testpass123')
        recipe = models.Recipe.objects.create(user=user,title='Sample recipe name',time_minutes=5,price=Decimal('5.50'),description='Sample recipe description')
        self.assertEqual(str(recipe),recipe.title)
    
    def test_create_tag(self):
        user = create_user()
        tag = models.Tag.objects.create(user=user,name='Tag1')
        self.assertEqual(str(tag),tag.name)
        