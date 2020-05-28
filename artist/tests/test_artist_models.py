from django.test import TestCase
from .. import models
from unittest.mock import patch
from main.tests.functions import sample_user, sample_artist, sample_song, mocked_song
from unittest import mock


class ArtistTest(TestCase):
    @mock.patch(
        "artist.models.functions.ArtistSpotifyAPI.get_artist",
        return_value="test_image_url",
    )
    def setUp(self, mock_get_spotify_image):
        self.user = sample_user()
        self.artist = sample_artist(self.user)

    def test_artist_str_representation(self):

        self.assertEqual(str(self.artist), self.artist.name)

    def test_name_capital_letter(self):

        self.assertEqual(self.artist.name, self.artist.name.title())

    @patch("uuid.uuid4")
    def test_artist_image_path(self, mock_uuid):
        uuid = "uuid_test"
        mock_uuid.return_value = uuid

        filename = "img.jpg"
        genereted_path = models.functions.artist_image_file_path(None, filename)

        expected_path = f"upload/artist/{uuid}.jpg"

        self.assertEqual(expected_path, genereted_path)

    @mock.patch(
        "song.models.functions.SongSpotifyAPI.get_song", return_value=mocked_song
    )
    @mock.patch(
        "song.models.functions.YoutubeAPI.get_video_url", return_value="test_video_url"
    )
    def test_correct_number_of_songs(self, mock_get_song, mock_get_video_url):
        sample_song(self.user, self.artist)
        sample_song(self.user, self.artist)

        self.assertEqual(self.artist.no_of_songs(), 2)

    @mock.patch(
        "song.models.functions.SongSpotifyAPI.get_song", return_value=mocked_song
    )
    @mock.patch(
        "song.models.functions.YoutubeAPI.get_video_url", return_value="test_video_url"
    )
    def test_incorrect_number_of_songs(self, mock_get_song, mock_get_video_url):
        sample_song(self.user, self.artist)

        self.assertNotEqual(self.artist.no_of_songs(), 2)

    def test_default_image_file_path(self):
        expected_path = "/media/upload/artist/default.jpeg"
        self.assertEqual(self.artist.image.url, expected_path)
