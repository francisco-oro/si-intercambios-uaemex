from django.db import models # noqa
"""
Database models.
"""
from django.db import models
from django.contrib.auth.models import (
    AbstractUser,
    BaseUserManager,
    PermissionsMixin
)


class UserManager(BaseUserManager):
    """Manager for user."""
    def create_user(self, account, password=None, **extra_fields):
        """Create, save and return a new user."""
        user = self.model(account=account, **extra_fields)
        user.set_password(password)
        user.save(using=self._db)

        return user



class User(AbstractUser, PermissionsMixin):
    """User information in the system"""
    account = models.CharField(max_length=7, unique=True)
    CURP = models.CharField(max_length=18)
    email = models.EmailField(unique=True) # VARCHAR
    name = models.CharField(max_length=255) # 
    last_name1 = models.CharField(max_length=255)
    last_name2 = models.CharField(max_length=255)
    gender = models.CharField(max_length=10)
    date_of_birth = models.DateField(null=True, blank=True)
    city = models.CharField(max_length=255)
    
    
    is_active = models.BooleanField(default=True)
    is_staff = models.BooleanField(default=False)
    
    objects = UserManager()
    
    USERNAME_FIELD = 'account'
    REQUIRED_FIELDS = ['email']


# https://django-improved-user.readthedocs.io/en/stable/create_custom_user_with_mixins.html