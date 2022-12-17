from django.db import models
from django.contrib.auth.models import (
    AbstractUser,
    BaseUserManager,
    PermissionsMixin,
)
from django.core.validators import RegexValidator

class UserManager(BaseUserManager):
    """Manager for users."""

    def create_user(self, phone, password=None, **extra_fields):
        """Create, save and return a new user."""
        user = self.model(phone=phone, **extra_fields)
        user.set_password(password)
        user.save()

        return user


class User(AbstractUser, PermissionsMixin):
    """User in the system."""
    phoneNumberRegex = RegexValidator(regex=r'^01([0|1|6|7|8|9]?)-?([0-9]{3,4})-?([0-9]{4})$')
    phone = models.CharField(validators=[phoneNumberRegex], max_length=11, unique=True)
    name = models.CharField(max_length=255)
    is_active = models.BooleanField(default=True)
    is_staff = models.BooleanField(default=False)
    is_superuser = models.BooleanField(default=False)

    objects = UserManager()

    USERNAME_FIELD = 'phone'