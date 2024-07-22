"""Tests for core models."""
from django.test import TestCase
from django.contrib.auth import get_user_model

class ModelTests(TestCase):
    """Test for core models."""
    
    def test_create_user_with_email_successful(self):
        """Test creating a new user with email is successful."""
        account = '1712239'
        password = 'testpass123'
        email = 'user@example.com'
        
        user = get_user_model().objects.create_user(
            account=account,
            password=password, 
            email=email
        )
        
        self.assertEqual(user.account, account)
        self.assertTrue(user.check_password(password))