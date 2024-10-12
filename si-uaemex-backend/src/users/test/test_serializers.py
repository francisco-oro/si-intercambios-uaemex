from django.test import TestCase
from django.contrib.auth.hashers import check_password
from nose.tools import eq_, ok_
from ..serializers import CreateUserSerializer, ProfileSerializer
from ..models import User


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

    # Perform
    def test_valid_profile_data(self):
        serializer = ProfileSerializer(data=self.profile_data)
        # Assert
        self.assertTrue(serializer.is_valid())

    # Perform
    def test_invalid_curp(self):
        self.profile_data['CURP'] = 'TOOLONG123456123456EFGHIJKL'
        serializer = ProfileSerializer(data=self.profile_data)
        # Assert
        self.assertFalse(serializer.is_valid())

    """Test that validation fails when an invalid string is provided as gender"""
    def test_invalid_gender(self):
        pass

    def test_underage_date_of_birth(self):
        pass