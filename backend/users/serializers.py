from django.contrib.auth import get_user_model
from rest_framework import serializers

User = get_user_model()


class UserCreateSerializer(serializers.ModelSerializer):
    password = serializers.CharField(write_only=True, min_length=4)

    class Meta:
        model = User
        fields = ["email", "full_name", "password"]

    def create(self, validated_data):
        email = validated_data["email"]
        full_name = validated_data.get("full_name", "")
        password = validated_data["password"]

        user = User.objects.create_user(
            username=email,
            email=email,
            password=password,
        )
        user.full_name = full_name
        user.is_staff = False
        user.save()
        return user


class UserLoginSerializer(serializers.Serializer):
    email = serializers.EmailField()
    password = serializers.CharField()


class UserReadSerializer(serializers.ModelSerializer):
    is_admin = serializers.BooleanField(source="is_staff", read_only=True)

    class Meta:
        model = User
        fields = ["id", "email", "full_name", "is_admin"]


class TokenSerializer(serializers.Serializer):
    access_token = serializers.CharField()
    token_type = serializers.CharField(default="bearer")