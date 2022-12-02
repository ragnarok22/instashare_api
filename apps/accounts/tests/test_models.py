from django.test import TestCase

from apps.accounts.models import User


class UserTest(TestCase):
    def setUp(self) -> None:
        self.user = User.objects.create_user(
            username="john", email="john@example.com", password="password1"
        )
        self.user_with_info = User.objects.create_user(
            username="patty",
            email="patty@example.com",
            password="patty123",
            first_name="Patricia",
            last_name="Gomez",
        )

    def test_convert_to_str_without_first_and_last_name(self):
        """get the full name from user who doesn't have first and last name"""
        self.assertEqual(str(self.user), self.user.username)

    def test_convert_to_str_with_first_and_last_name(self):
        """get the full name from user who have first and last name"""
        self.assertEqual(str(self.user_with_info), self.user_with_info.get_full_name())
