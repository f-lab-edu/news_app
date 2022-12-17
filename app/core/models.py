"""
Database models.
"""

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
        user.save(using=self._db)

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


class Category(models.Model):
    name = models.CharField(max_length=20)
    is_active = models.BooleanField(default=True)


class Topic(models.Model):
    category = models.ForeignKey(Category, on_delete=models.CASCADE)
    name = models.CharField(max_length=20)


class News(models.Model):
    topic1 = models.ForeignKey(Topic, on_delete=models.CASCADE, related_name='topic1')
    topic2 = models.ForeignKey(Topic, on_delete=models.CASCADE, related_name='topic2')
    topic3 = models.ForeignKey(Topic, on_delete=models.CASCADE, related_name='topic3')
    link = models.CharField(max_length=200)
    created_at = models.DateTimeField(auto_now_add=True)


class WeekUserTopic(models.Model):
    topic = models.ForeignKey(Topic, on_delete=models.CASCADE)
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    week = models.CharField(max_length=10)


class UserNews(models.Model):
    news = models.ForeignKey(News, on_delete=models.CASCADE)
    week_user_topic = models.ForeignKey(WeekUserTopic, on_delete=models.CASCADE)


class UserPage(models.Model):
    user_news1 = models.ForeignKey(UserNews, on_delete=models.CASCADE, related_name='user_news1')
    user_news2 = models.ForeignKey(UserNews, on_delete=models.CASCADE, related_name='user_news2')
    user_news3 = models.ForeignKey(UserNews, on_delete=models.CASCADE, related_name='user_news3')


class Alarm(models.Model):
    user_page = models.ForeignKey(UserPage, on_delete=models.CASCADE)
    send_date = models.DateTimeField()


class ReadingTime(models.Model):
    user_news = models.ForeignKey(UserNews, on_delete=models.CASCADE)
    reading_time = models.CharField(max_length=200)

