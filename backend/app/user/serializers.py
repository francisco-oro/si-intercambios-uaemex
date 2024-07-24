"""
Serializer for the user API view
"""

from rest_framework import serializers
from django.contrib.auth import get_user_model

class UserSerializer(serializers.ModelSerializer):
    """Serializer for the user API view"""

    class Meta:
        model = get_user_model()

        # TODO add fields that we get from RENAPO API
        fields = ('email', 'username', 'name', 'password')
        # TODO logic for password validation
        # Required rules - Password: min 8 & chars-number pass
        # Required rules - username: only numbers - max length 7
        extra_kwargs = {
            'password':
                {'min_length': 8},
        }

    def create(self, validated_data):
        """Create and return a new user with hashed password."""
        return get_user_model().objects.create_user(**validated_data)