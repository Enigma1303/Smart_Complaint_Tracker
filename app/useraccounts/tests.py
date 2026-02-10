from django.test import TestCase
from rest_framework import status
from django.urls import reverse
from django.contrib.auth import get_user_model
from rest_framework.test import APITestCase


class SignupAPITest(APITestCase):

    def test_signup_creates_user(self):
        url = reverse("signup")

        data = {
            "email": "signup@example.com",
            "password": "password123",
        }

        response = self.client.post(url, data)

        self.assertEqual(response.status_code, status.HTTP_201_CREATED)

        user = get_user_model().objects.get(email="signup@example.com")
        self.assertTrue(user.check_password("password123"))

    def test_signup_without_email_fails(self):
        url = reverse("signup")
        response = self.client.post(url, {"password": "123"})
        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)
 

class UserModelTest(TestCase):
    def test_create_user_with_email(self):
        user = get_user_model().objects.create_user(
            email="test@example.com",
            password="password123"
        )
        self.assertEqual(user.email, "test@example.com")
        self.assertTrue(user.check_password("password123"))

