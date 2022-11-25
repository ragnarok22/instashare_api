import os

from django.conf import settings
from django.db import models

from apps.core.models import TimeStampedModel
from apps.files.utils import human_file_size


def upload_to(instance, filename):
    return "images/{creator}/{filename}".format(
        creator=instance.creator, filename=filename
    )


class File(TimeStampedModel):
    creator = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE)
    title = models.CharField(max_length=100)
    file = models.FileField(upload_to=upload_to)

    def size(self) -> str:
        return human_file_size(os.stat(self.file.path).st_size)

    def __str__(self):
        return self.title.title()
