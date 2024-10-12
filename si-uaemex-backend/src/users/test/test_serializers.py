from django.test import TestCase
from django.contrib.auth.hashers import check_password
from nose.tools import eq_, ok_
from ..serializers import CreateUserSerializer, ProfileSerializer
from datetime import date
from dateutil.relativedelta import relativedelta

from django.contrib.auth import get_user_model

User = get_user_model()


class TestCreateUserSerializer(TestCase):
    def setUp(self):
        self.user_data = {'username': 'test', 'password': 'test'}

    def test_serializer_with_empty_data(self):
        serializer = CreateUserSerializer(data={})
        eq_(serializer.is_valid(), False)

    def test_serializer_with_valid_data(self):
        serializer = CreateUserSerializer(data=self.user_data)
        ok_(serializer.is_valid())

    def test_serializer_hashes_password(self):
        serializer = CreateUserSerializer(data=self.user_data)
        ok_(serializer.is_valid())

        user = serializer.save()
        ok_(check_password(self.user_data.get('password'), user.password))


"""Tests the validations performed by profile serializer"""
class ProfileSerializerTest(TestCase):
    # Arrange
    def setUp(self):
        self.user = User.objects.create_user(
            username='1278543',
            email='user@example.com',
            password='testpass123',
        )
        self.profile_data = {
            'CURP': "ABCD123456EFGHIJKL",
            'gender': "M",
            'date_of_birth': "1990-01-01",
            'city': 'Test City',
            'zip_code': '12345'
        }
        self.context = {'user': self.user}

    # Perform
    def test_valid_profile_data(self):
        serializer = ProfileSerializer(data=self.profile_data, context=self.context)
        # Assert
        self.assertTrue(serializer.is_valid())

    # Perform
    def test_invalid_curp(self):
        self.profile_data['CURP'] = 'TOOLONG123456123456EFGHIJKL'
        serializer = ProfileSerializer(data=self.profile_data, context=self.context)
        # Assert
        self.assertFalse(serializer.is_valid())

    """Test that validation fails when an invalid string is provided as gender"""
    def test_invalid_gender(self):
        pass

    def test_underage_date_of_birth(self):
        today = date.today()
        underage_date = today - relativedelta(years=17)
        self.profile_data['date_of_birth'] = underage_date
        serializer = ProfileSerializer(data=self.profile_data, context=self.context)
        self.assertFalse(serializer.is_valid())
        self.assertIn('date_of_birth', serializer.errors)

    def test_future_date_of_birth(self):
        today = date.today()
        future_date = today + relativedelta(years=17)
        self.profile_data['date_of_birth'] = future_date
        serializer = ProfileSerializer(data=self.profile_data, context=self.context)
        self.assertFalse(serializer.is_valid())
        self.assertIn('date_of_birth', serializer.errors)

    def test_invalid_zip_code(self):
        self.profile_data['zip_code'] = '1234'
        serializer = ProfileSerializer(data=self.profile_data, context=self.context)

        self.assertFalse(serializer.is_valid())

    def test_create_profile(self):
        serializer = ProfileSerializer(data=self.profile_data, context=self.context)
        self.assertTrue(serializer.is_valid())
        profile = serializer.save()
        self.assertIn(profile, Profile)
        self.assertEqual(profile.CURP, self.profile_data['CURP'])
        self.assertEqual(profile.gender, self.profile_data['gender'])
        self.assertEqual(profile.date_of_birth, self.profile_data['date_of_birth'])
        self.assertEqual(profile.city, self.profile_data['city'])
        self.assertEqual(profile.zip_code, self.profile_data['zip_code'])
