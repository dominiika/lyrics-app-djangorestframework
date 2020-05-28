from django.urls import reverse
from django.test import TestCase
from rest_framework import status
from rest_framework.test import APIClient

from ..models import Genre
from ..serializers import GenreSerializer
from main.tests.functions import (
    get_genre_detail_url,
    sample_user,
    sample_genre,
    sample_artist,
    sample_song,
    mocked_song,
)
from unittest import mock


GENRE_URL = reverse("main:genres-list")


class PublicGenreApiTests(TestCase):
    def setUp(self):
        self.client = APIClient()

    def test_retrieve_genres_success(self):

        user = sample_user()

        sample_genre(user, "Genre1")
        sample_genre(user, "Genre2")

        response = self.client.get(GENRE_URL)

        genres = Genre.objects.all()
        serializer = GenreSerializer(genres, many=True)

        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(response.data, serializer.data)

    def test_unauthorized_user_read_only(self):

        payload = {"user": "", "name": "rock"}
        response = self.client.post(GENRE_URL, payload)

        self.assertEqual(response.status_code, status.HTTP_401_UNAUTHORIZED)


class PrivateGenreApiTests(TestCase):
    def setUp(self):
        self.user = sample_user()
        self.client = APIClient()
        self.client.force_authenticate(self.user)

    def test_create_genre_success(self):
        payload = {"name": "Metal", "user": self.user.id}

        response = self.client.post(GENRE_URL, payload)

        genre = Genre.objects.get(id=response.data["id"])

        self.assertEqual(response.status_code, status.HTTP_201_CREATED)
        self.assertTrue(genre)

    def test_update_other_user_not_allowed(self):

        creator_user = sample_user("creator", "pass123")

        genre = sample_genre(creator_user)

        response = self.client.patch(
            get_genre_detail_url(genre.id), {"name": "updated genre"}
        )

        self.assertEqual(response.status_code, status.HTTP_403_FORBIDDEN)

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
    def test_retrieve_genres_assigned_to_song(
        self, mock_get_artist, mock_get_song, mock_get_video_url
    ):
        genre1 = sample_genre(self.user, "Genre1")
        genre2 = sample_genre(self.user, "Genre2")
        artist = sample_artist(self.user)
        song = sample_song(self.user, artist)
        song.genres.set([genre1])

        response = self.client.get(GENRE_URL, {"is_assigned": 1})

        serializer1 = GenreSerializer(genre1)
        serializer2 = GenreSerializer(genre2)

        self.assertIn(serializer1.data, response.data)
        self.assertNotIn(serializer2.data, response.data)

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
    def test_retrieve_unique_genres(
        self, mock_get_artist, mock_get_song, mock_get_video_url
    ):
        genre = sample_genre(self.user)
        artist = sample_artist(self.user)
        song1 = sample_song(self.user, artist, "Song1")
        song2 = sample_song(self.user, artist, "Song2")
        song1.genres.set([genre])
        song2.genres.set([genre])

        response = self.client.get(GENRE_URL, {"is_assigned": 1})

        self.assertEqual(len(response.data), 1)

    def test_user_assigned_automatically_post_method(self):
        payload = {
            "name": "Genre1",
        }

        response = self.client.post(GENRE_URL, payload)

        self.assertEqual(response.data["user"], self.user.id)
