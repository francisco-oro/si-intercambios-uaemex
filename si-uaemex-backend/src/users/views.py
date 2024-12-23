from rest_framework import viewsets, mixins
from rest_framework.permissions import AllowAny
from rest_framework.decorators import action
from rest_framework.response import Response
from rest_framework import status

from src.users.models import User, Profile
from src.users.permissions import IsUserOrReadOnly
from src.users.serializers import CreateUserSerializer, UserSerializer, ProfileSerializer

from src.common.events import EventHandler

import logging

logger = logging.getLogger(__name__)

class UserViewSet(mixins.RetrieveModelMixin, mixins.UpdateModelMixin, mixins.CreateModelMixin, viewsets.GenericViewSet):
    """
    Creates, Updates and Retrieves - User Accounts
    """

    queryset = User.objects.all()
    serializers = {'default': UserSerializer, 'create': CreateUserSerializer}
    permissions = {'default': (IsUserOrReadOnly,), 'create': (AllowAny,)}

    def get_serializer_class(self):
        return self.serializers.get(self.action, self.serializers['default'])

    def get_permissions(self):
        self.permission_classes = self.permissions.get(self.action, self.permissions['default'])
        return super().get_permissions()

    def perform_create(self, serializer):
        logger.info("Creating new user")
        try:
            user = serializer.save()
            logger.info(f"User created successfully: {user.email}")

            # Dispatch the user_created event
            logger.debug(f"Dispatching user_created event for user: {user.email}")
            EventHandler.dispatch('user_created', user)

        except Exception as e:
            logger.error(f"Error during user creation: {str(e)}")
            raise

    @action(detail=False, methods=['get'], url_path='me', url_name='me')
    def get_user_data(self, instance):
        try:
            return Response(UserSerializer(self.request.user, context={'request': self.request}).data, status=status.HTTP_200_OK)
        except Exception as e:
            return Response({'error': 'Wrong auth token' + e}, status=status.HTTP_400_BAD_REQUEST)


class ProfileViewSet(mixins.RetrieveModelMixin, mixins.UpdateModelMixin, mixins.CreateModelMixin, mixins.ListModelMixin, viewsets.GenericViewSet):
    """
    Creates, updated and Retrieves - User Profiles
    """
    queryset = Profile.objects.all()
    serializer_class = ProfileSerializer
