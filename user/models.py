from django.db import models
from django.contrib.auth.models import (
    AbstractUser,
    BaseUserManager,
    PermissionsMixin,
)
from django.core.validators import RegexValidator

import re


class UserManager(BaseUserManager):
    """Manager for users."""

    def create_user(self, phone, name, password=None):
        """Create, save and return a new user."""
        regex = r'^01([0|1|6|7|8|9]?)-?([0-9]{3,4})-?([0-9]{4})$'
        if not phone:
            raise ValueError('write phone number')
        if not re.match(regex, phone):
            raise ValueError('번호 형식을 맞춰주세요')
        if not name:
            raise ValueError('write name')
        if len(name) > 255:
            raise ValueError('255보다 짧게 입력해주세요')
        if not password:
            raise ValueError('write password')
        user = self.model(phone=phone, name=name, password=password)
        user.set_password(password)
        user.save()
        return user

    def create_superuser(self, phone, name, password=None):
        user = self.create_user(phone=phone, name=name, password=password)
        user.is_superuser = True
        user.save()
        return user


class User(AbstractUser, PermissionsMixin):
    """User in the system."""
    phoneNumberRegex = RegexValidator(regex=r'^01([0|1|6|7|8|9]?)-?([0-9]{3,4})-?([0-9]{4})$')
    phone = models.CharField(validators=[phoneNumberRegex], max_length=13, unique=True)
    name = models.CharField(max_length=255)
    is_active = models.BooleanField(default=True)
    is_superuser = models.BooleanField(default=False)

    objects = UserManager()

    REQUIRED_FIELDS = ['phone', 'name']