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
        data = {'name': 'DabApps'}
        response = self.client.post(CREATE_USER_URL, data, format='json')
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)
        # self.assertEqual(Account.objects.count(), 1)
        # self.assertEqual(Account.objects.get().name, 'DabApps')
        # factory = APIRequestFactory()
        # request = factory.post('/user/', )
        # print(request)
        # client = APIClient()
        # client.post()
