from django.contrib.auth.models import AbstractUser
from django.db import models


class User(AbstractUser):
    email = models.EmailField(unique=True)
    full_name = models.CharField(max_length=255, blank=True, null=True)

    @property
    def is_admin(self):
        return self.is_staff

    def __str__(self) -> str:
        return self.email