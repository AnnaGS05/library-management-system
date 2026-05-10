from rest_framework import serializers
from .models import Book


class BookReadSerializer(serializers.ModelSerializer):
    class Meta:
        model = Book
        fields = ["id", "title", "author", "year", "description", "available"]


class BookUpdateSerializer(serializers.ModelSerializer):
    class Meta:
        model = Book
        fields = ["title", "author", "year", "description", "available"]