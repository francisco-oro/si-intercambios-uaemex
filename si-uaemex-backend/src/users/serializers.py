from rest_framework import serializers
from rest_framework.validators import ValidationError
from datetime import date
from dateutil.relativedelta import relativedelta
from src.users.models import User, Profile
from src.common.serializers import ThumbnailerJSONSerializer
import re

from django.contrib.auth import get_user_model


class UserSerializer(serializers.ModelSerializer):
    profile_picture = ThumbnailerJSONSerializer(required=False, allow_null=True, alias_target='src.users')

    class Meta:
        model = User
        fields = (
            'id',
            'username',
            'first_name',
            'last_name',
            'last_name2',
            'profile_picture',
        )
        read_only_fields = ('username',)


class CreateUserSerializer(serializers.ModelSerializer):
    profile_picture = ThumbnailerJSONSerializer(required=False, allow_null=True, alias_target='src.users')
    tokens = serializers.SerializerMethodField()

    def get_tokens(self, user):
        return user.get_tokens()

    def create(self, validated_data):
        # call create_user on user object. Without this
        # the password will be stored in plain text.
        user = User.objects.create_user(**validated_data)
        return user

    class Meta:
        model = User
        fields = (
            'id',
            'username',
            'password',
            'first_name',
            'last_name',
            'email',
            'tokens',
            'profile_picture',
        )
        read_only_fields = ('tokens',)
        extra_kwargs = {'password': {'write_only': True}}


"""Serializer class for Profile serializer"""
class ProfileSerializer(serializers.ModelSerializer):
    user = serializers.PrimaryKeyRelatedField(queryset=User.objects.all())

    class Meta:
        model = Profile
        fields = ['id', 'user', 'CURP', 'gender', 'date_of_birth', 'city', 'zip_code']
    #
    # def validate_user(self, value):
    #     user = get_user_model().Objects.get(pk=value)
    #     if user is None:
    #         raise serializers.ValidationError('User not found')
    #     self.context['user'] = user
    #     return value

    def validate_CURP(self, value):
        if len(value) != 18:
            raise serializers.ValidationError('La CURP debe tener 18 caracteres')
        return value

    def validate_gender(self, value):
        valid_genders = ['M', 'F', 'O']
        if value not in valid_genders:
            raise ValidationError(f"El género sólo puede ser una de las siguientes opciones: {', '.join(valid_genders)}")
        return value

    def validate_date_of_birth(self, value):
        today = date.today()
        # age is expected to record the difference (ages)
        age = relativedelta(today, value).years

        if age < 18:
            raise ValidationError("Debes de tener al menos 18 años para aplicar a la beca")
        if age > 120 or age < 0:
            raise ValidationError("Por favor especifica una fecha de nacimiento válida")
        return value

    def validate_zip_code(self, value):
        zip_pattern = re.compile(r'^\d{5}$')
        if not zip_pattern.match(value):
            raise ValidationError('El código postal debe tener 5 dígitos')
        return value

    def create(self, validated_data):
        user = validated_data.pop('user')
        profile = Profile.objects.create(user=user, **validated_data)
        return profile