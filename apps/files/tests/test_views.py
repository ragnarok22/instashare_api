import json
import tempfile

from PIL import Image
from django.core.files import File as DjangoFile
from django.test.utils import override_settings
from django.urls import reverse
from rest_framework import status
from rest_framework.test import APITestCase

from apps.accounts.models import User
from apps.accounts.serializers import TokenSerializer
from apps.files.models import File, CompressedFile


class FileTests(APITestCase):
    """Tests for File app"""

    @staticmethod
    def create_user(username="user", email="user@example.com", password="password1"):
        user = User.objects.create_user(username, email, password)
        return user

    def get_token(self, user: User = None):
        user = user if user else self.user
        refresh = TokenSerializer.get_token(user)
        return str(refresh.access_token)

    def setUp(self) -> None:
        super().setUp()
        self.user = self.create_user()

    def test_create_a_file_with_anonymous_user(self):
        """Try to create a file without login"""
        url = reverse("file-list")

        image = Image.new("RGB", (100, 100))
        tmp_file = tempfile.NamedTemporaryFile(suffix=".jpg")
        image.save(tmp_file)
        tmp_file.seek(0)

        data = {"file": tmp_file, "title": "my image"}
        response = self.client.post(url, data, format="multipart")
        self.assertEqual(response.status_code, status.HTTP_401_UNAUTHORIZED)
        self.assertEqual(File.objects.count(), 0)

    @override_settings(
        CELERY_EAGER_PROPAGATES_EXCEPTIONS=True,
        CELERY_ALWAYS_EAGER=True,
        CELERY_BROKER_BACKEND="memory",
    )
    def test_create_a_file_with_register_user(self):
        """Try to create a file with authenticated user"""
        url = reverse("file-list")

        image = Image.new("RGB", (100, 100))
        tmp_file = tempfile.NamedTemporaryFile(suffix=".jpg")
        image.save(tmp_file)
        tmp_file.seek(0)
        image.save(tmp_file)
        tmp_file.seek(0)

        self.client.credentials(HTTP_AUTHORIZATION="Bearer " + self.get_token())

        data = {"title": "awesome image", "file": tmp_file}
        response = self.client.post(url, data, format="multipart")
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)
        self.assertEqual(File.objects.count(), 1)
        self.assertEqual(File.objects.get().title, data.get("title"))

    def test_list_no_files(self):
        """List files from user who has no files"""
        url = reverse("file-list")

        self.client.credentials(HTTP_AUTHORIZATION="Bearer " + self.get_token())
        response = self.client.get(url)

        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(json.loads(response.content).get("count"), 0)
        self.assertIsNone(json.loads(response.content).get("next"))
        self.assertIsNone(json.loads(response.content).get("previous"))
        self.assertEqual(json.loads(response.content).get("results"), [])

    def test_list_files_from_authenticated_user(self):
        """List files from user with one File"""
        url = reverse("file-list")

        # create a file
        image = Image.new("RGB", (100, 100))
        tmp_file = tempfile.NamedTemporaryFile(suffix=".jpg")
        image.save(tmp_file)
        tmp_file.seek(0)
        image.save(tmp_file)
        tmp_file.seek(0)
        file = File.objects.create(
            title="file 2", file=DjangoFile(tmp_file), creator=self.user
        )

        self.client.credentials(HTTP_AUTHORIZATION="Bearer " + self.get_token())
        response = self.client.get(url)

        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(json.loads(response.content).get("count"), 1)
        self.assertIsNone(json.loads(response.content).get("next"))
        self.assertIsNone(json.loads(response.content).get("previous"))
        self.assertEqual(len(json.loads(response.content).get("results")), 1)
        self.assertEqual(
            json.loads(response.content).get("results")[0].get("creator"),
            self.user.username,
        )
        self.assertEqual(
            json.loads(response.content).get("results")[0].get("creator_id"),
            self.user.id,
        )
        self.assertEqual(
            json.loads(response.content).get("results")[0].get("title"), file.title
        )

    def test_compress_file(self):
        """Send to compress all files for authenticated user"""
        url = reverse("file-compress")

        # create a file
        image = Image.new("RGB", (100, 100))
        tmp_file = tempfile.NamedTemporaryFile(suffix=".jpg")
        image.save(tmp_file)
        tmp_file.seek(0)
        image.save(tmp_file)
        tmp_file.seek(0)
        file = File.objects.create(
            title="file 2", file=DjangoFile(tmp_file), creator=self.user
        )

        self.client.credentials(HTTP_AUTHORIZATION="Bearer " + self.get_token())
        response = self.client.get(url)
        compress = CompressedFile.objects.filter(creator=self.user)

        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(
            json.loads(response.content).get("message"), "start processing"
        )
        self.assertEqual(compress.count(), 1)
        self.assertEqual(compress.first().creator, self.user)
