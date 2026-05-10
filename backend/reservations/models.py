from django.conf import settings
from django.db import models


class Reservation(models.Model):
    STATUS_CHOICES = [
        ("active", "Активно"),
        ("returned", "Возвращено"),
        ("cancelled", "Отменено"),
    ]

    user = models.ForeignKey(
        settings.AUTH_USER_MODEL,
        on_delete=models.CASCADE,
        related_name="reservations",
    )
    book = models.ForeignKey(
        "books.Book",
        on_delete=models.CASCADE,
        related_name="reservations",
    )
    reservation_date = models.DateTimeField(auto_now_add=True)
    status = models.CharField(
        max_length=20,
        choices=STATUS_CHOICES,
        default="active",
    )

    def __str__(self) -> str:
        return f"{self.user.email} -> {self.book.title}"