"""
URL Configuration for the user API.
"""

from django.urls import path
from user.views import CreateUserView

urlpatterns = [
    path('create', CreateUserView.as_view(), name='create'),
]