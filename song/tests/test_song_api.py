from django.urls import reverse
from django.test import TestCase
from rest_framework import status
from rest_framework.test import APIClient

from ..models import Song

from ..serializers import SongSerializer
from main.tests.functions import (
    sample_song,
    get_song_detail_url,
    sample_user,
    sample_artist,
    sample_genre,
    sample_rating,
    mocked_song,
)
from unittest import mock


SONG_URL = reverse("main:songs-list")


@mock.patch("song.models.functions.SongSpotifyAPI.get_song", return_value=mocked_song)
@mock.patch(
    "song.models.functions.YoutubeAPI.get_video_url", return_value="test_video_url"
)
class PublicSongApiTests(TestCase):
    @mock.patch(
        "artist.models.functions.ArtistSpotifyAPI.get_artist",
        return_value="test_image_url",
    )
    def setUp(self, mock_get_artist):
        self.client = APIClient()
        self.user = sample_user()
        self.artist = sample_artist(self.user)

    def test_retrieve_songs_success(self, mock_get_song, mock_get_video_url):

        sample_song(self.user, self.artist)
        sample_song(self.user, self.artist)

        response = self.client.get(SONG_URL)

        songs = Song.objects.all()
        serializer = SongSerializer(songs, many=True)

        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(response.data, serializer.data)

    def test_unauthorized_user_read_only(self, mock_get_song, mock_get_video_url):

        payload = {"artist": self.artist.id, "title": "test title"}

        response = self.client.post(SONG_URL, payload)

        self.assertEqual(response.status_code, status.HTTP_401_UNAUTHORIZED)


@mock.patch("song.models.functions.SongSpotifyAPI.get_song", return_value=mocked_song)
@mock.patch(
    "song.models.functions.YoutubeAPI.get_video_url", return_value="test_video_url"
)
class PrivateSongApiTests(TestCase):
    @mock.patch(
        "artist.models.functions.ArtistSpotifyAPI.get_artist",
        return_value="test_image_url",
    )
    def setUp(self, mock_get_artist):
        self.user = sample_user()
        self.client = APIClient()
        self.client.force_authenticate(self.user)
        self.artist = sample_artist(self.user)

    def test_create_song_success(self, mock_get_song, mock_get_video_url):

        payload = {
            "user": self.user.id,
            "artist": self.artist.id,
            "title": "test title",
        }

        response = self.client.post(SONG_URL, payload)

        song = Song.objects.get(id=response.data["id"])

        self.assertEqual(response.status_code, status.HTTP_201_CREATED)
        self.assertTrue(song)

    def test_update_other_user_success(self, mock_get_song, mock_get_video_url):

        creator_user = sample_user("creator", "pass123")

        song = sample_song(creator_user, self.artist)

        response = self.client.patch(
            get_song_detail_url(song.id), {"title": "brand new title"}
        )

        song.refresh_from_db()

        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(response.data["title"], song.title)
        self.assertTrue(song.edited)
        self.assertNotEqual(song.edited_at_time, song.created_at_time)
        self.assertEqual(song.edited_by_user, self.user)

    def test_delete_other_user_not_allowed(self, mock_get_song, mock_get_video_url):

        creator_user = sample_user("creator", "pass123")

        song = sample_song(creator_user, self.artist)

        response = self.client.delete(get_song_detail_url(song.id))

        self.assertEqual(response.status_code, status.HTTP_403_FORBIDDEN)

    @mock.patch(
        "artist.models.functions.ArtistSpotifyAPI.get_artist",
        return_value="test_image_url",
    )
    def test_filter_songs_by_artist(
        self, mock_get_song, mock_get_video_url, mock_get_artist
    ):
        artist2 = sample_artist(self.user, "Artist2")

        song1 = sample_song(self.user, self.artist, "Title1")
        song2 = sample_song(self.user, artist2, "Title2")

        response = self.client.get(SONG_URL, {"artist": f"{artist2.id}"})

        serializer1 = SongSerializer(song1)
        serializer2 = SongSerializer(song2)

        self.assertIn(serializer2.data, response.data)
        self.assertNotIn(serializer1.data, response.data)

    def test_filter_songs_by_genre(self, mock_get_song, mock_get_video_url):

        genre1 = sample_genre(self.user, "Genre1")
        genre2 = sample_genre(self.user, "Genre2")

        song1 = sample_song(self.user, self.artist, "Title1")
        song2 = sample_song(self.user, self.artist, "Title2")

        song1.genres.set([genre1])
        song2.genres.set([genre2])

        response = self.client.get(SONG_URL, {"genre": f"{genre1.id}"})

        serializer1 = SongSerializer(song1)
        serializer2 = SongSerializer(song2)

        self.assertIn(serializer1.data, response.data)
        self.assertNotIn(serializer2.data, response.data)

    def test_user_assigned_automatically_post_method(
        self, mock_get_song, mock_get_video_url
    ):
        payload = {"title": "Test title", "artist": self.artist.id}

        response = self.client.post(SONG_URL, payload)

        self.assertEqual(response.data["user"], self.user.id)

    def test_user_assigned_automatically_put_method(
        self, mock_get_song, mock_get_video_url
    ):
        user2 = sample_user("user2", "pass123")
        song = sample_song(user2, self.artist)

        payload = {"title": "Updated title", "artist": self.artist.id}

        response = self.client.put(get_song_detail_url(song.id), payload)

        self.assertEqual(response.data["edited_by_user"], self.user.id)

    def test_get_latest_songs(self, mock_get_song, mock_get_video_url):
        song1 = sample_song(self.user, self.artist, "Song1")
        song2 = sample_song(self.user, self.artist, "Song2")
        song3 = sample_song(self.user, self.artist, "Song3")

        response = self.client.get(SONG_URL, {"latest": 2})

        serializer1 = SongSerializer(song1)
        serializer2 = SongSerializer(song2)
        serializer3 = SongSerializer(song3)

        self.assertIn(serializer2.data, response.data)
        self.assertIn(serializer3.data, response.data)
        self.assertNotIn(serializer1.data, response.data)

    def test_get_highest_rated_songs(self, mock_get_song, mock_get_video_url):
        song1 = sample_song(self.user, self.artist, "Song1")
        song2 = sample_song(self.user, self.artist, "Song2")
        song3 = sample_song(self.user, self.artist, "Song3")

        sample_rating(self.user, song1, 5)
        sample_rating(self.user, song2, 4)
        sample_rating(self.user, song3, 1)

        response = self.client.get(SONG_URL, {"highest": 2})

        serializer1 = SongSerializer(song1)
        serializer2 = SongSerializer(song2)
        serializer3 = SongSerializer(song3)

        self.assertIn(serializer1.data, response.data)
        self.assertIn(serializer2.data, response.data)
        self.assertNotIn(serializer3.data, response.data)
