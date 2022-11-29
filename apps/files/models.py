import os

from django.conf import settings
from django.db import models

from apps.core.models import TimeStampedModel
from apps.files.utils import human_file_size


def upload_to(instance, filename):
    return "{creator}/files/{filename}".format(
        creator=instance.creator.username, filename=filename
    )


def upload_compressed_to(instance, filename):
    return "{creator}/compressed/{filename}".format(
        creator=instance.creator.username, filename=filename
    )


class File(TimeStampedModel):
    creator = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE)
    title = models.CharField(max_length=100)
    file = models.FileField(upload_to=upload_to)

    def size(self) -> str:
        return human_file_size(os.stat(self.file.path).st_size)

    def __str__(self):
        return self.title.title()


class CompressedFile(TimeStampedModel):
    """
    Store the compressed files. Only exists 24 hours
    """

    creator = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE)
    file = models.FileField(upload_to=upload_compressed_to, null=True, blank=True)
    is_finish = models.BooleanField(default=False)
    task_id = models.CharField(max_length=200)

    class Meta:
        ordering = ["-updated_at", "-created_at"]
