from django.contrib.auth.models import AbstractUser

from django.db import models


def upload_to(instance, filename):
    return "{user}/pictures/{filename}".format(
        user=instance.username, filename=filename
    )


class User(AbstractUser):
    """
    User model
    """

    about = models.CharField(max_length=150, null=True, blank=True)
    github = models.URLField(null=True, blank=True)
    twitter = models.URLField(null=True, blank=True)
    picture = models.ImageField(null=True, blank=True, upload_to=upload_to)

    class Meta:
        ordering = ["username"]

    def __str__(self) -> str:
        return self.get_full_name() or self.username
