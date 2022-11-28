from django.contrib.auth.models import AbstractUser

from django.db import models


class User(AbstractUser):
    """
    User model
    """

    about = models.CharField(max_length=150, null=True, blank=True)
    github = models.URLField(null=True, blank=True)
    twitter = models.URLField(null=True, blank=True)

    class Meta:
        ordering = ["username"]

    def __str__(self) -> str:
        return self.get_full_name() or self.username
