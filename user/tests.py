from rest_framework.test import APITestCase
from user.models import User
from django.urls import reverse
from rest_framework import status
from django.contrib.auth import get_user_model

import json


class SignUpTest(APITestCase):

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

    def test_create_superuser(self):
        """test creating a superuser"""
        user = get_user_model().objects.create_superuser(
            '01-0111--111',
            'aaaa',
            '11'
        )
        self.assertTrue(user.is_superuser)

