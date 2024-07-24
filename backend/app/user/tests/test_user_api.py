"""
Tests for the user API.
"""
from django.contrib.auth import get_user_model
from django.urls import reverse
from django.test import TestCase

from rest_framework import status
from rest_framework.test import APIClient

CREATE_USER_URL = reverse('user:create')

def create_user(**params):
    """Create and return a new user."""
    return get_user_model().objects.create_user(**params)


class PublicUserApiTests(TestCase):
    """Test the publicly available user API"""

    def setUp(self) -> None:
        self.client = APIClient()

    def test_create_valid_user_success(self):
        """Test creating user with valid payload is successful."""
        payload = {
            'username': '1723394',
            'email': 'test@example.com',
            'password': 'testpass123',
            'name': 'Test'
        }
        res = self.client.post(CREATE_USER_URL, payload)
        self.assertEqual(res.status_code, status.HTTP_201_CREATED)
        user = get_user_model().objects.get(username=payload['username'])
        self.assertTrue(user.check_password(payload['password']))
        self.assertNotIn('password', res.data)

    def test_create_user_username_already_exists_error(self):
        """Test creating a user that already exists fails."""
        payload = {
            'username': '5892825',
            'email': 'guest@example.com',
            'password': 'testpass123',
            'name': 'Test'
        }
        create_user(**payload)
        res = self.client.post(CREATE_USER_URL, payload)
        self.assertEqual(res.status_code, status.HTTP_400_BAD_REQUEST)

    def test_create_user_email_already_exists_error(self):
        """Test creating a user with an email address that already exists fails."""
        payload_1 = {
            'username': '5892825',
            'email': 'guest@example.com',
            'password': 'testpass123',
            'name': 'Test'
        }

        payload_2 = {
            'username': '2810384',
            'email': 'guest@example.com',
            'password': 'testpass123',
            'name': 'Test 2'
        }

        create_user(**payload_1)
        res = self.client.post(CREATE_USER_URL, payload_2)
        self.assertEqual(res.status_code, status.HTTP_400_BAD_REQUEST)

    def test_password_too_short_error(self):
        """Test that a user cannot be created with a weak password:
        Password must be at least 8 characters long. At least a number is required
        """
        payload_1 = {
            'username': '5892825',
            'email': 'guest@example.com',
            'password': 'lopwzwer',
            'name': 'Test'
        }

        payload_2 = {
            'username': '2810384',
            'email': 'guest@example.com',
            'password': 'test3',
            'name': 'Test 2'
        }

        res_1 = self.client.post(CREATE_USER_URL, payload_1)
        res_2 = self.client.post(CREATE_USER_URL, payload_2)

        self.assertEqual(res_1.status_code, status.HTTP_400_BAD_REQUEST)
        self.assertEqual(res_2.status_code, status.HTTP_400_BAD_REQUEST)