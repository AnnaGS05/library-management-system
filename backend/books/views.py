from django.db.models import Q
from rest_framework import permissions, status
from rest_framework.response import Response
from rest_framework.views import APIView

from .models import Book
from .serializers import BookReadSerializer, BookUpdateSerializer


class IsAdminUserCustom(permissions.BasePermission):
    def has_permission(self, request, view):
        if request.method in permissions.SAFE_METHODS:
            return True
        return bool(
            request.user
            and request.user.is_authenticated
            and request.user.is_staff
        )


class BooksView(APIView):
    permission_classes = [IsAdminUserCustom]

    def get(self, request):
        q = request.query_params.get("q")
        queryset = Book.objects.all().order_by("id")

        if q:
            queryset = queryset.filter(
                Q(title__icontains=q) | Q(author__icontains=q)
            )

        return Response(BookReadSerializer(queryset, many=True).data)

    def post(self, request):
        serializer = BookUpdateSerializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        book = serializer.save()
        return Response(
            BookReadSerializer(book).data,
            status=status.HTTP_201_CREATED,
        )


class BookDetailView(APIView):
    permission_classes = [IsAdminUserCustom]

    def get_object(self, book_id):
        try:
            return Book.objects.get(id=book_id)
        except Book.DoesNotExist:
            return None

    def get(self, request, book_id):
        book = self.get_object(book_id)
        if not book:
            return Response({"detail": "Book not found"}, status=404)
        return Response(BookReadSerializer(book).data)

    def put(self, request, book_id):
        book = self.get_object(book_id)
        if not book:
            return Response({"detail": "Book not found"}, status=404)

        serializer = BookUpdateSerializer(book, data=request.data)
        serializer.is_valid(raise_exception=True)
        serializer.save()

        return Response(BookReadSerializer(book).data)

    def delete(self, request, book_id):
        book = self.get_object(book_id)
        if not book:
            return Response({"detail": "Book not found"}, status=404)

        book.delete()
        return Response({"detail": "Book deleted"}, status=200)