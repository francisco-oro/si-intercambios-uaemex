from django.urls import reverse
from django.contrib.auth.hashers import check_password
from nose.tools import ok_, eq_
from rest_framework.test import APITestCase
from rest_framework import status
from faker import Faker
from ..models import User, Profile
from ..serializers import ProfileSerializer
from .factories import UserFactory

from django.contrib.auth import get_user_model


fake = Faker()

class TestUserListTestCase(APITestCase):
    """
    Tests /users list operations.
    """

    def setUp(self):
        self.url = reverse('user-list')
        self.user_data = {'username': '1284273', 'password': 'test',
                          'email': 'user@example.com', 'first_name': 'john', 'last_name': 'doe'}

    def test_post_request_with_no_data_fails(self):
        response = self.client.post(self.url, {})
        eq_(response.status_code, status.HTTP_400_BAD_REQUEST)

    def test_post_request_with_valid_data_succeeds(self):
        response = self.client.post(self.url, self.user_data)
        eq_(response.status_code, status.HTTP_201_CREATED)

        user = User.objects.get(pk=response.data.get('id'))
        eq_(user.username, self.user_data.get('username'))
        ok_(check_password(self.user_data.get('password'), user.password))


class TestUserDetailTestCase(APITestCase):
    """
    Tests /users detail operations.
    """

    def setUp(self):
        self.user = UserFactory()
        tokens = self.user.get_tokens()
        access_token = tokens['access']
        self.url = reverse('user-detail', kwargs={'pk': self.user.pk})
        self.client.credentials(HTTP_AUTHORIZATION=f'Bearer {access_token}')

    def test_get_request_returns_a_given_user(self):
        response = self.client.get(self.url)
        eq_(response.status_code, status.HTTP_200_OK)

    def test_put_request_updates_a_user(self):
        new_first_name = fake.first_name()
        new_last_name = fake.last_name()
        new_last_name2 = fake.last_name()
        payload = {'first_name': new_first_name, 'last_name': new_last_name, 'last_name2': new_last_name2}
        response = self.client.put(self.url, payload)
        eq_(response.status_code, status.HTTP_200_OK)

        user = User.objects.get(pk=self.user.id)
        eq_(user.first_name, new_first_name)


class TestListProfileTestCase(APITestCase):
    """
    Tests /users list profile operations.
    """

    def setUp(self):
        self.user = UserFactory()
        if hasattr(self.user, 'profile'):
            self.user.profile.delete()
        self.url = reverse('profile-list')  # Adjust this to match your URL configuration
        self.profile_data = {
            'user': self.user.id,
            'CURP': "ABCD123456EFGHIJKL",
            'gender': "M",
            'date_of_birth': "1990-01-01",
            'city': 'Test City',
            'zip_code': '12345'
        }

        tokens = self.user.get_tokens()
        access_token = tokens['access']
        self.client.credentials(HTTP_AUTHORIZATION=f'Bearer {access_token}')

    def test_create_profile(self):
        """Test a profile is being created succesfully"""
        response = self.client.post(self.url, self.profile_data)
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)
        self.assertTrue(Profile.objects.filter(user=self.user).exists())

    def test_get_request_returns_a_given_profile(self):
        response = self.client.get(self.url)
        eq_(response.status_code, status.HTTP_200_OK)


class TestProfileUpdate(APITestCase):
    def setUp(self):
        self.user = UserFactory()
        if hasattr(self.user, 'profile'):
            self.user.profile.delete()
        self.profile = Profile.objects.create(
            user=self.user,
            CURP="ABCD123456EFGHIJKL",
            gender="M",
            date_of_birth="1990-01-01",
            city="Old City",
            zip_code="12345"
        )
        self.url = reverse('profile-detail', kwargs={'pk': self.profile.pk})

        tokens = self.user.get_tokens()
        access_token = tokens['access']
        self.client.credentials(HTTP_AUTHORIZATION=f'Bearer {access_token}')

    def test_put_profile_update(self):
        updated_data = {
            'user': self.user.id,
            'CURP': "EFGH987654IJKLMNOP",
            'gender': "F",
            'date_of_birth': "1995-05-05",
            'city': "New City",
            'zip_code': "67890"
        }
        response = self.client.put(self.url, updated_data)
        self.assertEqual(response.status_code, status.HTTP_200_OK)

        self.profile.refresh_from_db()
        self.assertEqual(self.profile.CURP, updated_data['CURP'])
        self.assertEqual(self.profile.gender, updated_data['gender'])
        self.assertEqual(self.profile.date_of_birth, parse_date(updated_data['date_of_birth']))
        self.assertEqual(self.profile.city, updated_data['city'])

    def test_patch_profile_update(self):
        patch_data = {
            'city': "Patched City",
            'zip_code': "54321"
        }
        response = self.client.patch(self.url, patch_data)
        self.assertEqual(response.status_code, status.HTTP_200_OK)

        self.profile.refresh_from_db()
        self.assertEqual(self.profile.city, patch_data['city'])
        self.assertEqual(self.profile.CURP, "ABCD123456EFGHIJKL")
        self.assertEqual(self.profile.gender, "M")
        self.assertEqual(self.profile.date_of_birth, parse_date("1990-01-01"))

    def test_put_profile_update_invalid_data(self):
        invalid_data = {
            'user': self.user.id,
            'CURP': "INVALID_CURP",  # Invalid CURP
            'gender': "Invalid",  # Invalid gender
            'date_of_birth': "2025-01-01",  # Future date
            'city': "New City",
            'zip_code': "1234"  # Invalid zip code
        }
        response = self.client.put(self.url, invalid_data)
        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)
        self.assertIn('CURP', response.data)
        self.assertIn('gender', response.data)
        self.assertIn('date_of_birth', response.data)
        self.assertIn('zip_code', response.data)

    def test_patch_profile_update_unauthenticated(self):
        self.client.force_authenticate(user=None)
        patch_data = {'city': "Unauthorized City"}
        response = self.client.patch(self.url, patch_data)
        self.assertEqual(response.status_code, status.HTTP_401_UNAUTHORIZED)