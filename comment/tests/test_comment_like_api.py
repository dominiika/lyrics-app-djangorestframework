from django.test import TestCase
from django.urls import reverse
from rest_framework import status
from rest_framework.test import APIClient
from main.tests.functions import (
    sample_user,
    sample_artist,
    sample_song,
    sample_comment,
    sample_comment_like,
    get_comment_like_detail_url,
    mocked_song,
)
from ..models import CommentLike
from ..serializers import CommentLikeSerializer
from unittest import mock


COMMENT_LIKE_URL = reverse("main:comment_likes-list")


class PublicCommentLikeApiTest(TestCase):
    @mock.patch(
        "artist.models.functions.ArtistSpotifyAPI.get_artist",
        return_value="test_image_url",
    )
    @mock.patch(
        "song.models.functions.SongSpotifyAPI.get_song", return_value=mocked_song
    )
    @mock.patch(
        "song.models.functions.YoutubeAPI.get_video_url", return_value="test_video_url"
    )
    def setUp(self, mock_get_artist, mock_get_song, mock_get_video_url):
        self.client = APIClient()
        self.user = sample_user()
        self.artist = sample_artist(self.user)
        self.song = sample_song(self.user, self.artist)
        self.comment = sample_comment(self.user, self.song)

    def test_retrieve_comments_success(self):

        sample_comment_like(self.user, self.comment)

        response = self.client.get(COMMENT_LIKE_URL)

        likes = CommentLike.objects.all()
        serializer = CommentLikeSerializer(likes, many=True)

        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(response.data, serializer.data)


class PrivateCommentLikeApiTest(TestCase):
    @mock.patch(
        "artist.models.functions.ArtistSpotifyAPI.get_artist",
        return_value="test_image_url",
    )
    @mock.patch(
        "song.models.functions.SongSpotifyAPI.get_song", return_value=mocked_song
    )
    @mock.patch(
        "song.models.functions.YoutubeAPI.get_video_url", return_value="test_video_url"
    )
    def setUp(self, mock_get_artist, mock_get_song, mock_get_video_url):
        self.client = APIClient()
        self.user = sample_user()
        self.client.force_authenticate(self.user)
        self.artist = sample_artist(self.user)
        self.song = sample_song(self.user, self.artist)
        self.comment = sample_comment(self.user, self.song)

    def test_post_method_not_allowed(self):
        payload = {"comment": self.comment.id}

        response = self.client.post(COMMENT_LIKE_URL, payload)

        self.assertEqual(response.status_code, status.HTTP_405_METHOD_NOT_ALLOWED)

    def test_put_method_not_allowed(self):
        like = sample_comment_like(self.user, self.comment)
        response = self.client.put(get_comment_like_detail_url(like.id))

        self.assertEqual(response.status_code, status.HTTP_405_METHOD_NOT_ALLOWED)
