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
