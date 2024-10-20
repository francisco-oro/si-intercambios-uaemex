from rest_framework.routers import SimpleRouter

from src.users.views import UserViewSet, ProfileViewSet

users_router = SimpleRouter()

users_router.register(r'users', UserViewSet)
users_router.register(r'profiles', ProfileViewSet)
