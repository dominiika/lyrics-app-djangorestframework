from rest_framework import serializers
from .models import Artist
from genre.models import Genre
from django.contrib.auth import get_user_model
from django.core.exceptions import ValidationError


class ArtistSerializer(serializers.ModelSerializer):

    user = serializers.PrimaryKeyRelatedField(
        queryset=get_user_model().objects.all(), required=False
    )
    user_str = serializers.CharField(source="user", read_only=True)

    genres = serializers.PrimaryKeyRelatedField(
        queryset=Genre.objects.all(), many=True, required=False
    )
    genres_str = serializers.StringRelatedField(
        many=True, read_only=True, source="genres"
    )

    def validate_genres(self, value):
        if len(value) > 4:
            raise ValidationError("Only 4 genres are allowed.")
        return value

    class Meta:
        model = Artist
        fields = (
            "id",
            "user",
            "name",
            "image",
            "genres",
            "genres_str",
            "user_str",
            "no_of_songs",
            "spotify_image",
        )

        read_only_fields = ("id",)


class ArtistImageSerializer(serializers.ModelSerializer):
    class Meta:
        model = Artist
        fields = ("id", "image")
        read_only_fields = ("id",)
