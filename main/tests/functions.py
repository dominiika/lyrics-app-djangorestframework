from django.urls import reverse
from django.contrib.auth import get_user_model
from song.models import Song, Rating
from artist.models import Artist
from genre.models import Genre
from comment.models import Comment, CommentLike

ARTIST_URL = reverse("main:artists-list")

GENRE_URL = reverse("main:genres-list")

SONG_URL = reverse("main:songs-list")

mocked_song = {
    "album_name": "test_album_name",
    "album_image": "test_album_image_url",
    "song_id": "test_song_id",
}


def get_artist_url_detail(pk):
    artist_detail_url = reverse("main:artists-detail", kwargs={"pk": pk})
    return artist_detail_url


def get_song_detail_url(pk):
    song_detail_url = reverse("main:songs-detail", kwargs={"pk": pk})
    return song_detail_url


def get_genre_detail_url(pk):
    genre_detail_url = reverse("main:genres-detail", kwargs={"pk": pk})
    return genre_detail_url


def get_like_url(comment_id):
    return reverse("main:comments-like", args=[comment_id])


def get_comment_like_detail_url(pk):
    comment_like_detail_url = reverse("main:comment_likes-detail", kwargs={"pk": pk})
    return comment_like_detail_url


def get_user_detail_url(pk):
    user_detail_url = reverse("user:users-detail", kwargs={"pk": pk})
    return user_detail_url


def sample_user(
    username="sample", password="samplepass", email="sample@email.com",
):
    return get_user_model().objects.create_user(
        username=username, password=password, email=email
    )


def sample_genre(user, name="test genre"):
    genre = Genre.objects.create(user=user, name=name)
    return genre


def sample_artist(user, name="testname"):
    artist = Artist.objects.create(user=user, name=name,)
    return artist


def sample_song(user, artist, title="sampletitle"):
    song = Song.objects.create(user=user, artist=artist, title=title)
    return song


def sample_comment(user, song, content="Test content"):
    comment = Comment.objects.create(user=user, song=song, content=content)
    return comment


def sample_comment_like(user, comment):
    comment_like = CommentLike.objects.create(user=user, comment=comment)
    return comment_like


def sample_rating(user, song, points):
    rating = Rating.objects.create(user=user, song=song, points=points)
    return rating
