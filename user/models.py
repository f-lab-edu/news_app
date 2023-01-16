from django.db import models
from django.contrib.auth.models import (
    AbstractUser,
    BaseUserManager,
    PermissionsMixin,
)
from django.core.validators import RegexValidator

from django.db.models import Count
from django.db import transaction

from topic.models import Topic


class UserManager(BaseUserManager):
    """Manager for users."""

    @transaction.atomic()
    def create(self, phone, name, password, category1, category2, category3):
        user = self.model(phone=phone, name=name, password=password)
        user.set_password(password)

        topic_queryset = Topic.objects.filter()
        category1_cnt = topic_queryset.filter(category=category1).values('category', 'name').annotate(
            category_cnt=Count('category')).order_by('category_cnt')[0]
        category2_cnt = topic_queryset.filter(category=category2).values('category', 'name').annotate(
            category_cnt=Count('category')).order_by('category_cnt')[0]
        category3_cnt = topic_queryset.filter(category=category3).values('category', 'name').annotate(
            category_cnt=Count('category')).order_by('category_cnt')[0]

        topic1 = category1_cnt['name']
        topic2 = category2_cnt['name']
        topic3 = category3_cnt['name']

        user.save()
        return topic1, topic2, topic3


class User(AbstractUser, PermissionsMixin):
    """User in the system."""
    phoneNumberRegex = RegexValidator(regex=r'^01([0|1|6|7|8|9]?)-?([0-9]{3,4})-?([0-9]{4})$')
    phone = models.CharField(validators=[phoneNumberRegex], max_length=13, unique=True)
    name = models.CharField(max_length=255)
    is_active = models.BooleanField(default=True)
    is_superuser = models.BooleanField(default=False)

    objects = UserManager()

    REQUIRED_FIELDS = ['phone', 'name']