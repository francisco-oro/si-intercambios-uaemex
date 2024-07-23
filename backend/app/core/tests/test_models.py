"""Tests for core models."""
from django.test import TestCase
from django.contrib.auth import get_user_model
from django.db.utils import IntegrityError

from psycopg2.errors import UniqueViolation
class ModelTests(TestCase):
    """Test for core models."""

    def test_create_user_with_email_successful(self):
        """Test creating a new user with email and account number is successful."""
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

    def test_new_user_email_normalized(self):
        """Test the email for a new user is normalized"""
        email = 'medo@TESTUSER.COM'
        account = '9608624'
        user = get_user_model().objects.create_user(account, 'test123', email=email)

        self.assertEqual(user.email, email.lower())

    def test_new_user_without_account_raises_error(self):
        """Test that creating a user without account raises error."""
        with self.assertRaises(ValueError):
            user = get_user_model().objects.create_user('', 'sample123')

    def test_new_user_without_email_raises_error(self):
        """Test that creating a user without email raises error."""
        with self.assertRaises(ValueError):
            user = get_user_model().objects.create_user('1712237', 'sample123')

    def test_create_superuser(self):
        """Test creating a superuser."""
        user = get_user_model().objects.create_superuser(
            '1712235',
            'test123',
            email='admin@example.com'
        )

        self.assertTrue(user.is_superuser)
        self.assertTrue(user.is_staff)


