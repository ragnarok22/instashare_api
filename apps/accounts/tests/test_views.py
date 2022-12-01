import json

from django.urls import reverse
from rest_framework.test import APITestCase

from apps.accounts.models import User
from apps.accounts.serializers import TokenSerializer
from rest_framework import status


class AccountTests(APITestCase):
    """Test for Accounts app"""

    @staticmethod
    def create_user(
        username="user",
        email="user@example.com",
        password="password1",
        is_superuser=False,
    ):
        user = User.objects.create_user(
            username, email, password, is_superuser=is_superuser
        )
        return user

    def get_token(self, user: User = None):
        user = user if user else self.user
        refresh = TokenSerializer.get_token(user)
        return str(refresh.access_token)

    def setUp(self) -> None:
        self.user = self.create_user()

    def test_get_user_list_from_anonymous_user(self):
        """Get user list from anonymous user"""
        url = reverse("user-list")

        response = self.client.get(url)

        self.assertEqual(response.status_code, status.HTTP_401_UNAUTHORIZED)

    def test_get_user_list(self):
        """Get user list from normal user"""
        url = reverse("user-list")

        self.client.credentials(HTTP_AUTHORIZATION="Bearer " + self.get_token())
        response = self.client.get(url)

        self.assertEqual(response.status_code, status.HTTP_403_FORBIDDEN)

    def test_get_user_list_from_admin(self):
        """Get user list from admin user"""
        url = reverse("user-list")
        user = User.objects.get(username="admin")

        self.client.credentials(HTTP_AUTHORIZATION="Bearer " + self.get_token(user))
        response = self.client.get(url)

        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(json.loads(response.content).get("count"), 2)
        self.assertIsNone(json.loads(response.content).get("next"))
        self.assertIsNone(json.loads(response.content).get("previous"))
        self.assertEqual(len(json.loads(response.content).get("results")), 2)

    def test_get_current_user_info_without_logged_user(self):
        """Get the info from the logged user with anonymous user"""
        url = reverse("user-me")

        response = self.client.get(url)

        self.assertEqual(response.status_code, status.HTTP_401_UNAUTHORIZED)
        self.assertEqual(
            json.loads(response.content).get("detail"),
            "Authentication credentials were not provided.",
        )

    def test_get_current_user_info(self):
        """Get the info from the logged user"""
        url = reverse("user-me")

        self.client.credentials(HTTP_AUTHORIZATION="Bearer " + self.get_token())

        response = self.client.get(url)

        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(json.loads(response.content).get("id"), self.user.id)
        self.assertEqual(
            json.loads(response.content).get("username"), self.user.username
        )
        self.assertEqual(
            json.loads(response.content).get("first_name"), self.user.first_name
        )
        self.assertEqual(
            json.loads(response.content).get("last_name"), self.user.last_name
        )
        self.assertEqual(json.loads(response.content).get("email"), self.user.email)
        self.assertEqual(json.loads(response.content).get("about"), self.user.about)
        self.assertEqual(json.loads(response.content).get("twitter"), self.user.twitter)
        self.assertEqual(json.loads(response.content).get("github"), self.user.github)
        self.assertEqual(json.loads(response.content).get("picture"), self.user.picture)

    def test_register_user(self):
        """Register a new user"""
        url = reverse("register")

        data = {
            "username": "john",
            "first_name": "John",
            "last_name": "Doe",
            "email": "john@example.com",
            "password": "myPassword123",
            "password2": "myPassword123",
        }

        response = self.client.post(url, data)

        self.assertEqual(response.status_code, status.HTTP_201_CREATED)
        self.assertEqual(
            json.loads(response.content).get("username"), data.get("username")
        )
        self.assertEqual(
            json.loads(response.content).get("first_name"), data.get("first_name")
        )
        self.assertEqual(
            json.loads(response.content).get("last_name"), data.get("last_name")
        )
        self.assertEqual(json.loads(response.content).get("email"), data.get("email"))

    def test_register_user_with_short_password(self):
        """Register a new user with short password"""
        url = reverse("register")

        data = {
            "username": "john",
            "first_name": "John",
            "last_name": "Doe",
            "email": "john@example.com",
            "password": "pass",
            "password2": "pass",
        }

        response = self.client.post(url, data)

        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)
        self.assertEqual(
            json.loads(response.content).get("password"),
            [
                "This password is too short. It must contain at least 8 characters.",
                "This password is too common.",
            ],
        )

    def test_register_user_with_missing_email(self):
        """Register a new user with short password"""
        url = reverse("register")

        data = {
            "username": "john",
            "first_name": "John",
            "last_name": "Doe",
            "password": "myPass123Ultra",
            "password2": "myPass123Ultra",
        }

        response = self.client.post(url, data)

        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)
        self.assertEqual(
            json.loads(response.content).get("email"), ["This field is required."]
        )
