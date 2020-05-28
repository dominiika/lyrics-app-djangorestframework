from rest_framework import serializers
from django.contrib.auth import get_user_model
from .models import Song, Rating
from artist.models import Artist
from genre.models import Genre
from django.core.exceptions import ValidationError


class SongSerializer(serializers.ModelSerializer):

    artist = serializers.PrimaryKeyRelatedField(queryset=Artist.objects.all())
    artist_str = serializers.CharField(source="artist", read_only=True)

    genres = serializers.PrimaryKeyRelatedField(queryset=Genre.objects.all(), many=True)
    genres_str = serializers.StringRelatedField(
        many=True, read_only=True, source="genres"
    )

    user = serializers.PrimaryKeyRelatedField(
        queryset=get_user_model().objects.all(), required=False
    )
    user_str = serializers.CharField(source="user", read_only=True)

    edited_by_user = serializers.PrimaryKeyRelatedField(
        queryset=get_user_model().objects.all(), required=False
    )
    edited_by_user_str = serializers.SerializerMethodField("get_user_str")

    @staticmethod
    def get_user_str(song):
        try:
            return song.edited_by_user.username
        except:
            return None

    def validate_genres(self, value):
        if len(value) > 4:
            raise ValidationError("Only 4 genres are allowed.")
        return value

    class Meta:
        model = Song
        fields = (
            "id",
            "user",
            "user_str",
            "artist",
            "artist_str",
            "title",
            "genres",
            "genres_str",
            "lyrics",
            "created_at_time",
            "created_date_short",
            "edited",
            "edited_date_short",
            "edited_at_time",
            "edited_by_user",
            "edited_by_user_str",
            "no_of_ratings",
            "avg_rating",
            "no_of_comments",
            "image",
            "spotify_song_id",
            "spotify_album_name",
            "spotify_album_image",
            "youtube_video_url",
        )
        extra_kwargs = {
            "user": {"read_only": True},
            "created_at_time": {"read_only": True},
            "edited": {"read_only": True},
            "edited_at_time": {"read_only": True},
            "edited_by_user": {"read_only": True},
        }


class SongDetailSerializer(SongSerializer):

    artist = serializers.PrimaryKeyRelatedField(queryset=Artist.objects.all(),)
    artist_str = serializers.CharField(source="artist", read_only=True)

    genres = serializers.PrimaryKeyRelatedField(queryset=Genre.objects.all(), many=True)
    genres_str = serializers.StringRelatedField(
        many=True, read_only=True, source="genres"
    )


class RatingSerializer(serializers.ModelSerializer):

    user = serializers.PrimaryKeyRelatedField(queryset=get_user_model().objects.all())
    user_str = serializers.CharField(source="user", read_only=True)

    song = serializers.PrimaryKeyRelatedField(queryset=Song.objects.all())
    song_str = serializers.CharField(source="song", read_only=True)

    class Meta:
        model = Rating
        fields = ("id", "points", "user", "song", "user_str", "song_str")
