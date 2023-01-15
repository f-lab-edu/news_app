from rest_framework.test import APITestCase, APIClient, APIRequestFactory
from user.models import User
from django.urls import reverse
from rest_framework import status
from django.contrib.auth import get_user_model
from django.test import TestCase

import json

CREATE_USER_URL = reverse('user-list')


class Test(APITestCase):

    def test_create(self):
        pass
