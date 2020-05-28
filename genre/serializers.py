from rest_framework import serializers
from .models import Genre
from django.contrib.auth import get_user_model


class GenreSerializer(serializers.ModelSerializer):
    user = serializers.PrimaryKeyRelatedField(
        queryset=get_user_model().objects.all(), required=False
    )
    user_str = serializers.CharField(source="user", read_only=True)

    class Meta:
        model = Genre
        fields = ("id", "user", "name", "user_str")
        read_only_fields = ("id",)
