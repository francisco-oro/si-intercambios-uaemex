"""
Tests for Django admin modifications
"""
from django.db import transaction
from django.test import TestCase
from django.contrib.auth import get_user_model
from django.urls import reverse
from django.test import Client
from django.db.utils import IntegrityError

from psycopg2.errors import UniqueViolation

class AdminSiteTests(TestCase):
    """Tests for admin site."""

    def setUp(self):
        """Create user and client"""
        try:
            self.client = Client()
            with transaction.atomic():
                self.admin_user = get_user_model().objects.create_superuser(
                    email='admin@example.com',
                    password='testpass123',
                    account='1712231'
                )

            self.client.force_login(self.admin_user)
            self.user = get_user_model().objects.create_user(
                email='user@example.com',
                password='testpass123',
                account='1712232'
            )
        except (IntegrityError, UniqueViolation):
            print("User already exists.")

    def test_users_listed(self):
        """Test that users are listed on user page."""
        url = reverse('admin:core_user_changelist')
        res = self.client.get(url)

        self.assertContains(res, self.user.account)
        self.assertContains(res, self.user.email)