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


class CommentTest(TestCase):
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

    def test_short_comment_str_representation(self):
        comment = sample_comment(self.user, self.song)

        self.assertEqual(str(comment), comment.content)

    def test_long_comment_str_representation(self):
        comment = sample_comment(
            self.user,
            self.song,
            "Lorem ipsum dolor sit amet, consectetur adipiscing elit. Sed at elit lacus. Proin "
            "egestas vestibulum tortor, et volutpat felis efficitur non. Aenean ultrices, dolor "
            "vehicula accumsan varius, lectus elit rhoncus nisl, ac tempus nulla tortor vel urna. "
            "Phasellus eget felis ut libero dictum facilisis nec ut augue. ",
        )

        self.assertEqual(len(str(comment)), 53)

    def test_correct_number_of_likes(self):
        user2 = sample_user("user2", "pass123")
        comment = sample_comment(self.user, self.song)

        sample_comment_like(self.user, comment)
        sample_comment_like(user2, comment)

        self.assertEqual(comment.no_of_likes(), 2)

    def test_incorrect_number_of_likes(self):
        user2 = sample_user("user2", "pass123")
        comment = sample_comment(self.user, self.song)

        sample_comment_like(self.user, comment)
        sample_comment_like(user2, comment)

        self.assertNotEqual(comment.no_of_likes(), 1)
