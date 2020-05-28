from django.db import models
from django.contrib.auth import get_user_model
from django.core.validators import MaxValueValidator, MinValueValidator
from django.db.models import Avg
from artist.models import Artist
from genre.models import Genre
from .functions import (
    save_spotify_album_image,
    save_spotify_album_name,
    save_spotify_song_id,
    get_youtube_data,
    get_number_of_items,
)


BASE_URL = "http://127.0.0.1:8000"


class Song(models.Model):
    user = models.ForeignKey(
        get_user_model(), on_delete=models.CASCADE, related_name="songs"
    )
    artist = models.ForeignKey(Artist, on_delete=models.CASCADE, related_name="songs")
    title = models.CharField(max_length=60)
    genres = models.ManyToManyField(Genre)
    lyrics = models.TextField(blank=True)

    created_at_time = models.DateTimeField(auto_now_add=True,)

    edited = models.BooleanField(default=False)
    edited_at_time = models.DateTimeField(auto_now=True)
    edited_by_user = models.ForeignKey(
        get_user_model(),
        on_delete=models.CASCADE,
        related_name="edited_songs",
        blank=True,
        null=True,
    )
    spotify_song_id = models.CharField(max_length=150, blank=True, null=True)
    spotify_album_name = models.CharField(max_length=150, blank=True, null=True)
    spotify_album_image = models.CharField(max_length=255, blank=True, null=True)
    youtube_video_url = models.CharField(max_length=255, blank=True, null=True)

    def save(self, *args, **kwargs):
        title = getattr(self, "title", False)
        if title:
            setattr(self, "title", title.title())

        self.spotify_song_id = save_spotify_song_id(self)
        self.spotify_album_name = save_spotify_album_name(self)
        self.spotify_album_image = save_spotify_album_image(self)
        self.youtube_video_url = get_youtube_data(self)

        super(Song, self).save(*args, **kwargs)

    def created_date_short(self):
        return self.created_at_time.strftime("%d.%m.%Y, %H:%M")

    def edited_date_short(self):
        return self.edited_at_time.strftime("%d.%m.%Y, %H:%M")

    def image(self):
        try:
            return self.artist.image
        except:
            return None

    def avg_rating(self):
        avg = self.ratings.all().aggregate(Avg("points"))

        if avg["points__avg"] is None:
            avg["points__avg"] = 0
        return round(avg["points__avg"], 1)

    def no_of_ratings(self):
        return get_number_of_items(self.ratings)

    def no_of_comments(self):
        return get_number_of_items(self.comments)

    class Meta:
        ordering = ["title"]

    def __str__(self):
        return self.title


class Rating(models.Model):
    song = models.ForeignKey(Song, on_delete=models.CASCADE, related_name="ratings")
    user = models.ForeignKey(get_user_model(), on_delete=models.CASCADE)
    points = models.IntegerField(
        validators=[MinValueValidator(1), MaxValueValidator(5)]
    )

    class Meta:
        unique_together = (("user", "song"),)
        index_together = (("user", "song"),)

    def __str__(self):
        name = "{0.user} - {0.song}"
        return name.format(self)
