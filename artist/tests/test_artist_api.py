from django.urls import reverse
from django.test import TestCase
from rest_framework import status
from rest_framework.test import APIClient
from artist.models import Artist
from main.tests.functions import (
    get_artist_url_detail,
    sample_user,
    sample_song,
    sample_artist,
    mocked_song,
)
from unittest import mock


ARTIST_URL = reverse("main:artists-list")


@mock.patch(
    "artist.models.functions.ArtistSpotifyAPI.get_artist", return_value="test_image_url"
)
class PublicArtistApiTests(TestCase):
    def setUp(self):
        self.client = APIClient()

    def test_retrieve_artists_success(self, mock_get_spotify_image):
        user = sample_user()

        sample_artist(user, "Artist1")
        sample_artist(user, "Artist2")

        response = self.client.get(ARTIST_URL)

        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(len(response.data), 2)

    def test_unauthorized_user_read_only(self, mock_get_spotify_image):

        payload = {
            "name": "testname",
        }

        response = self.client.post(ARTIST_URL, payload)

        self.assertEqual(response.status_code, status.HTTP_401_UNAUTHORIZED)


@mock.patch(
    "artist.models.functions.ArtistSpotifyAPI.get_artist", return_value="test_image_url"
)
class PrivateArtistApiTests(TestCase):
    def setUp(self):

        self.user = sample_user()
        self.client = APIClient()
        self.client.force_authenticate(self.user)

    def test_create_artist_success(self, mock_get_spotify_image):

        payload = {"name": "testname", "user": self.user.id}

        response = self.client.post(ARTIST_URL, payload)

        artist = Artist.objects.get(id=response.data["id"])

        self.assertEqual(response.status_code, status.HTTP_201_CREATED)
        self.assertTrue(artist)

    def test_update_other_user_not_allowed(self, mock_get_spotify_image):

        owner_user = sample_user(username="owner")
        artist = sample_artist(owner_user)

        payload = {
            "name": "editedname",
        }

        response = self.client.patch(get_artist_url_detail(artist.id), payload)

        self.assertEqual(response.status_code, status.HTTP_403_FORBIDDEN)

    @mock.patch(
        "song.models.functions.SongSpotifyAPI.get_song", return_value=mocked_song
    )
    @mock.patch(
        "song.models.functions.YoutubeAPI.get_video_url", return_value="test_video_url"
    )
    def test_retrieve_unique_artists(
        self, mock_get_spotify_image, mock_get_song, mock_get_video_url
    ):
        artist = sample_artist(self.user)

        sample_song(self.user, artist, "Song1")
        sample_song(self.user, artist, "Song2")

        response = self.client.get(ARTIST_URL, {"is_assigned": 1})

        self.assertEqual(len(response.data), 1)

    def test_user_assigned_automatically_post_method(self, mock_get_spotify_image):
        payload = {
            "name": "Artist1",
        }

        response = self.client.post(ARTIST_URL, payload)

        self.assertEqual(response.data["user"], self.user.id)
