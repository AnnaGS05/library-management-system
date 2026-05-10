from django.db import models


class Book(models.Model):
    title = models.CharField(max_length=255, db_index=True)
    author = models.CharField(max_length=255, db_index=True)
    year = models.IntegerField(blank=True, null=True)
    description = models.TextField(blank=True, null=True)
    available = models.BooleanField(default=True)

    def __str__(self) -> str:
        return self.title