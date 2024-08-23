"""
Serializer for the user API view
"""

from rest_framework import serializers
from django.contrib.auth import get_user_model
from rest_framework.validators import UniqueValidator


class UserSerializer(serializers.ModelSerializer):
    """Serializer for the user API view"""
    email = serializers.EmailField(required=True,
                                   validators=[UniqueValidator(queryset=get_user_model().objects.all())])
    username = serializers.CharField(required=True, max_length=10,
        validators=[UniqueValidator(queryset=get_user_model().objects.all())])
    password = serializers.CharField(write_only=True, required=True, min_length=8)
    confirm_password = serializers.CharField(write_only=True, required=True, min_length=8)
    CURP = serializers.CharField(max_length=18,
                                 validators=[UniqueValidator(queryset=get_user_model().objects.all())])
    last_name1 = serializers.CharField(max_length=60)
    last_name2 = serializers.CharField(max_length=60)
    gender = serializers.ChoiceField(choices=["H", "M"])
    date_of_birth = serializers.DateField(format="%d-%m-%Y")

    class Meta:
        model = get_user_model()
        fields = ('CURP', 'username', 'name',
                  'password', 'last_name1', 'last_name2', 'gender', 'date_of_birth')

    def create(self, validated_data):
        """Create and return a new user with hashed password."""
        return get_user_model().objects.create_user(**validated_data)

# https://www.django-rest-framework.org/api-guide/serializers/