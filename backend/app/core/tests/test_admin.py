"""
Tests for Django admin modifications
"""
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
            self.admin_user = get_user_model().objects.create_superuser(
                email='admin@example.com',
                password='testpass123',
                username='1812231'
            )

            self.client.force_login(self.admin_user)
            self.user = get_user_model().objects.create_user(
                email='user@example.com',
                password='testpass123',
                username='1812232'
            )

        except (IntegrityError, UniqueViolation):
            print("User already exists.")

    def test_users_listed(self):
        """Test that users are listed on user page."""
        url = reverse('admin:core_user_changelist')
        res = self.client.get(url)

        self.assertContains(res, self.user.username)
        self.assertContains(res, self.user.email)

    def test_edit_user_page(self):
        """Test that the user edit page works."""
        url = reverse('admin:core_user_change', args=[self.user.id])
        res = self.client.get(url)
        self.assertEqual(res.status_code, 200)

    def test_create_user_page(self):
        """Test that the user create page works."""
        url = reverse('admin:core_user_add')
        res = self.client.get(url)

        self.assertEqual(res.status_code, 200)
