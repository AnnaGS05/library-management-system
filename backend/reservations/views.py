from rest_framework import permissions, status
from rest_framework.response import Response
from rest_framework.views import APIView

from books.models import Book
from .models import Reservation
from .serializers import ReservationCreateSerializer, ReservationReadSerializer


class ReservationCreateView(APIView):
    permission_classes = [permissions.IsAuthenticated]

    def post(self, request):
        serializer = ReservationCreateSerializer(data=request.data)
        serializer.is_valid(raise_exception=True)

        book_id = serializer.validated_data["book_id"]

        try:
            book = Book.objects.get(id=book_id)
        except Book.DoesNotExist:
            return Response(
                {"detail": "Book not found"},
                status=status.HTTP_404_NOT_FOUND,
            )

        if not book.available:
            return Response(
                {"detail": "Book is not available"},
                status=status.HTTP_400_BAD_REQUEST,
            )

        reservation = Reservation.objects.create(
            user=request.user,
            book=book,
            status="active",
        )

        book.available = False
        book.save()

        return Response(
            ReservationReadSerializer(reservation).data,
            status=status.HTTP_201_CREATED,
        )


class MyReservationsView(APIView):
    permission_classes = [permissions.IsAuthenticated]

    def get(self, request):
        reservations = Reservation.objects.filter(user=request.user).order_by("-reservation_date")
        return Response(ReservationReadSerializer(reservations, many=True).data)