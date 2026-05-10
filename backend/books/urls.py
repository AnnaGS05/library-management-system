from django.urls import path
from .views import BooksView, BookDetailView

urlpatterns = [
    path("", BooksView.as_view(), name="books"),
    path("<int:book_id>", BookDetailView.as_view(), name="book_detail"),
]