from django.test import TestCase
from main.tests.functions import (
    sample_user,
    sample_comment,
    sample_song,
    sample_artist,
    sample_comment_like,
    mocked_song,
)
from unittest import mock


class CommentLikeTest(TestCase):
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
        self.user = sample_user()
        self.artist = sample_artist(self.user)
        self.song = sample_song(self.user, self.artist)
        self.comment = sample_comment(self.user, self.song)

    def test_str_representation(self):
        comment_like = sample_comment_like(self.user, self.comment)

        self.assertEqual(str(comment_like), f"{self.user} - {self.comment}")
