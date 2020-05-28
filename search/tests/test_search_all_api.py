from django.urls import reverse
from django.test import TestCase
from rest_framework import status
from rest_framework.test import APIClient
from main.tests.functions import (
    sample_user,
    sample_genre,
    sample_artist,
    sample_song,
    mocked_song,
)
from genre.serializers import GenreSerializer
from artist.serializers import ArtistSerializer
from song.serializers import SongSerializer
from unittest import mock


SEARCH_URL = reverse("search:search-all")


class SearchAllTest(TestCase):
    def setUp(self):
        self.user = sample_user()
        self.client = APIClient()

    def test_genres_search(self):
        genre1 = sample_genre(self.user, "Rock")
        genre2 = sample_genre(self.user, "Progressive Metal")

        response = self.client.get(SEARCH_URL, {"value": "metal", "page_number": 1})

        serializer1 = GenreSerializer(genre1)
        serializer2 = GenreSerializer(genre2)

        self.assertIn(serializer2.data, response.data["genres"])
        self.assertNotIn(serializer1.data, response.data["genres"])

    @mock.patch(
        "artist.models.functions.ArtistSpotifyAPI.get_artist",
        return_value="test_image_url",
    )
    def test_artists_search(self, mock_get_artist):
        artist1 = sample_artist(self.user, "The Doors")
        artist2 = sample_artist(self.user, "Haken")

        response = self.client.get(SEARCH_URL, {"value": "doors", "page_number": 1})

        serializer1 = ArtistSerializer(artist1)
        serializer2 = ArtistSerializer(artist2)

        self.assertIn(serializer1.data, response.data["artists"])
        self.assertNotIn(serializer2.data, response.data["artists"])

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
    def test_songs_search(self, mock_get_artist, mock_get_song, mock_get_video_url):
        artist = sample_artist(self.user, "The Doors")
        song1 = sample_song(self.user, artist, "The End")
        song2 = sample_song(self.user, artist, "Light my fire")

        response = self.client.get(SEARCH_URL, {"value": "fire", "page_number": 1})

        serializer1 = SongSerializer(song1)
        serializer2 = SongSerializer(song2)

        self.assertIn(serializer2.data, response.data["songs"])
        self.assertNotIn(serializer1.data, response.data["songs"])

    def test_search_wrong_parameter(self):

        response = self.client.get(SEARCH_URL, {"val": "fire", "page_number": 1})

        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)

    def test_search_no_page_number(self):

        response = self.client.get(SEARCH_URL, {"value": "fire"})

        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)

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
    def test_songs_attached_to_genre(
        self, mock_get_artist, mock_get_song, mock_get_video_url
    ):
        genre1 = sample_genre(self.user, "Rock")
        genre2 = sample_genre(self.user, "Psychodelic rock")
        artist = sample_artist(self.user, "The Doors")
        song1 = sample_song(self.user, artist, "The End")
        song2 = sample_song(self.user, artist, "Light my fire")
        song1.genres.set([genre1])
        song2.genres.set([genre2])

        response = self.client.get(
            SEARCH_URL, {"value": "psychodelic", "page_number": 1}
        )

        serializer1 = SongSerializer(song1)
        serializer2 = SongSerializer(song2)

        self.assertIn(serializer2.data, response.data["songs"])
        self.assertNotIn(serializer1.data, response.data["songs"])

    @mock.patch(
        "artist.models.functions.ArtistSpotifyAPI.get_artist",
        return_value="test_image_url",
    )
    def test_artists_attached_to_genre(self, mock_get_artist):
        genre1 = sample_genre(self.user, "Rock")
        genre2 = sample_genre(self.user, "Progressive metal")
        artist1 = sample_artist(self.user, "The Doors")
        artist2 = sample_artist(self.user, "Haken")
        artist1.genres.set([genre1])
        artist2.genres.set([genre2])

        response = self.client.get(
            SEARCH_URL, {"value": "progressive", "page_number": 1}
        )

        serializer1 = ArtistSerializer(artist1)
        serializer2 = ArtistSerializer(artist2)

        self.assertIn(serializer2.data, response.data["artists"])
        self.assertNotIn(serializer1.data, response.data["artists"])
