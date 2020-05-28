from rest_framework import serializers
from song.models import Song
from .models import Comment, CommentLike
from django.contrib.auth import get_user_model


class CommentSerializer(serializers.ModelSerializer):

    user = serializers.PrimaryKeyRelatedField(
        queryset=get_user_model().objects.all(), required=False
    )
    user_str = serializers.CharField(source="user", read_only=True)

    song = serializers.PrimaryKeyRelatedField(queryset=Song.objects.all())
    song_str = serializers.CharField(source="song", read_only=True)

    class Meta:
        model = Comment
        fields = (
            "id",
            "song",
            "user",
            "user_str",
            "song_str",
            "content",
            "created_at_time",
            "edited_at_time",
            "edited",
            "no_of_likes",
        )


class CommentLikeSerializer(serializers.ModelSerializer):

    user = serializers.PrimaryKeyRelatedField(
        queryset=get_user_model().objects.all(), required=False
    )
    user_str = serializers.CharField(source="user", read_only=True)

    comment = serializers.PrimaryKeyRelatedField(queryset=Comment.objects.all())
    comment_str = serializers.CharField(source="comment", read_only=True)

    class Meta:
        model = CommentLike
        fields = ("id", "comment", "user", "user_str", "comment_str")
