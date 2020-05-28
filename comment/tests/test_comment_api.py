from django.urls import reverse
from django.test import TestCase
from rest_framework import status
from rest_framework.test import APIClient
from main.tests.functions import (
    get_like_url,
    sample_user,
    sample_artist,
    sample_song,
    sample_comment,
    mocked_song,
)
from ..models import Comment
from ..serializers import CommentSerializer
from unittest import mock


COMMENT_URL = reverse("main:comments-list")


class PublicCommentApiTest(TestCase):
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

    def test_retrieve_comments_success(self):

        sample_comment(self.user, self.song, "Test comment1")
        sample_comment(self.user, self.song, "Test comment2")

        response = self.client.get(COMMENT_URL)

        comments = Comment.objects.all()
        serializer = CommentSerializer(comments, many=True)

        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(response.data, serializer.data)

    def test_unauthorized_user_read_only(self):

        payload = {"song": self.song.id, "content": "Test content"}
        response = self.client.post(COMMENT_URL, payload)

        self.assertEqual(response.status_code, status.HTTP_401_UNAUTHORIZED)

    def test_unauthorized_like_not_allowed(self):
        comment = sample_comment(self.user, self.song)
        url = get_like_url(comment.id)

        response = self.client.post(url)

        self.assertEqual(response.status_code, status.HTTP_401_UNAUTHORIZED)


class PrivateCommentApiTest(TestCase):
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

    def test_user_assigned_automatically_post_method(self):
        payload = {"song": self.song.id, "content": "Test content"}

        response = self.client.post(COMMENT_URL, payload)

        self.assertEqual(response.data["user"], self.user.id)

    def test_like(self):
        url = get_like_url(self.comment.id)

        response = self.client.post(url)

        expected_msg = "The comment has been liked."

        self.assertEqual(response.data["message"], expected_msg)
        self.assertEqual(response.status_code, status.HTTP_200_OK)

    def test_dislike(self):
        url = get_like_url(self.comment.id)

        self.client.post(url)
        response = self.client.post(url)

        expected_msg = "The comment has been disliked."

        self.assertEqual(response.data["message"], expected_msg)
        self.assertEqual(response.status_code, status.HTTP_204_NO_CONTENT)
