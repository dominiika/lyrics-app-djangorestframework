from django.urls import reverse
from django.test import TestCase
from rest_framework import status
from rest_framework.test import APIClient
from main.tests.functions import (
    sample_song,
    sample_user,
    sample_artist,
    sample_rating,
    mocked_song,
)
from ..models import Rating
from ..serializers import RatingSerializer, SongSerializer
from unittest import mock


RATING_URL = reverse("main:ratings-list")


class PublicRatingApiTest(TestCase):
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

    def test_retrieve_ratings_success(self):

        sample_rating(self.user, self.song, 5)

        response = self.client.get(RATING_URL)

        ratings = Rating.objects.all()
        serializer = RatingSerializer(ratings, many=True)

        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(response.data["results"], serializer.data)

    def test_unauthorized_user_read_only(self):

        url = reverse("main:songs-rate", args=[self.song.id])
        response = self.client.post(url, {"points": 5})

        self.assertEqual(response.status_code, status.HTTP_401_UNAUTHORIZED)


class PrivateRatingApiTest(TestCase):
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
        self.client.force_authenticate(self.user)

    def test_user_assigned_automatically_post_method(self):

        url = reverse("main:songs-rate", args=[self.song.id])
        response = self.client.post(url, {"points": 5})

        self.assertEqual(response.data["result"]["user"], self.user.id)

    def test_rate_song(self):

        url = reverse("main:songs-rate", args=[self.song.id])
        self.client.post(url, {"points": 5})

        serializer = SongSerializer(self.song)

        self.assertEqual(serializer.data["avg_rating"], 5.0)
        self.assertEqual(serializer.data["no_of_ratings"], 1)

    def test_rate_song_update(self):

        sample_rating(self.user, self.song, 4)

        url = reverse("main:songs-rate", args=[self.song.id])
        self.client.post(url, {"points": 5})

        serializer = SongSerializer(self.song)

        self.assertEqual(serializer.data["avg_rating"], 5.0)
        self.assertEqual(serializer.data["no_of_ratings"], 1)

    def test_rate_song_no_points_provided(self):

        url = reverse("main:songs-rate", args=[self.song.id])
        response = self.client.post(url, {})

        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)

    def test_get_rate(self):

        rating = sample_rating(self.user, self.song, 5)
        url = reverse("main:ratings-get-rate")
        payload = {"user": self.user.id, "song": self.song.id}
        response = self.client.post(url, payload)

        serializer = RatingSerializer(rating)

        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(serializer.data, response.data["result"])

    def test_get_rate_no_results(self):

        url = reverse("main:ratings-get-rate")
        payload = {"user": self.user.id, "song": self.song.id}
        response = self.client.post(url, payload)

        self.assertEqual(response.status_code, status.HTTP_404_NOT_FOUND)

    def test_get_rate_no_song(self):

        sample_rating(self.user, self.song, 5)
        url = reverse("main:ratings-get-rate")
        payload = {
            "user": self.user.id,
        }
        response = self.client.post(url, payload)

        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)

    def test_get_rate_no_user(self):

        sample_rating(self.user, self.song, 5)
        url = reverse("main:ratings-get-rate")
        payload = {"song": self.song.id}
        response = self.client.post(url, payload)

        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)
