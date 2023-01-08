from rest_framework.test import APITestCase, APIClient
from user.models import User
from django.urls import reverse
from rest_framework import status
from django.contrib.auth import get_user_model
from django.test import TestCase

import json

CREATE_USER_URL = reverse('user-list')


class SignUpTest(APITestCase):

    def setUp(self):
        self.client = APIClient()

    def test_create_user(self):
        """tests creating a user"""
        phone = '010-1112-1111'
        name = '11'
        password = '1234'
        user = get_user_model().objects.create_user(
            phone=phone,
            name=name,
            password=password
        )

        self.assertEqual(user.phone, phone)
        self.assertEqual(user.name, name)
        # self.assertEqual(user.password, password)

    def test_create_user_success(self):
        """Test creating a user is successful."""
        payload = {
            'phone': '010-1111-1111',
            'name': 'Name',
            'password': '11'
        }
        res = self.client.post(CREATE_USER_URL, payload)

        self.assertEqual(res.status_code, status.HTTP_201_CREATED)
        user = get_user_model().objects.get(
            phone=payload['phone'],
            name=payload['name'],
            password=payload['password']
        )
        self.assertTrue(user.check_password(payload['password']))
        self.assertNotIn('password', res.data)

    def test_create_superuser(self):
        """test creating a superuser"""
        user = get_user_model().objects.create_superuser(
            '010-0111-1111',
            'aaaa',
            '11'
        )
        self.assertTrue(user.is_superuser)

