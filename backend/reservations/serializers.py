from rest_framework import serializers
from .models import Reservation


class ReservationCreateSerializer(serializers.Serializer):
    book_id = serializers.IntegerField()


class ReservationReadSerializer(serializers.ModelSerializer):
    book_id = serializers.IntegerField(source="book.id", read_only=True)
    user_id = serializers.IntegerField(source="user.id", read_only=True)
    created_at = serializers.DateTimeField(source="reservation_date", read_only=True)

    class Meta:
        model = Reservation
        fields = ["id", "book_id", "user_id", "created_at"]