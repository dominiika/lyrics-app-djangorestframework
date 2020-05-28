from django.db import models
from django.contrib.auth import get_user_model
from genre.models import Genre
from .functions import get_spotify_image


class Artist(models.Model):
    user = models.ForeignKey(get_user_model(), on_delete=models.CASCADE)
    name = models.CharField(max_length=60)
    image = models.CharField(max_length=255, null=True, blank=True)
    genres = models.ManyToManyField(Genre)
    spotify_image = models.TextField(blank=True, null=True)

    def save(self, *args, **kwargs):
        val = getattr(self, "name", False)
        if val:
            setattr(self, "name", val.title())
        self.spotify_image = get_spotify_image(self)
        if not self.image:
            self.image = 'https://i.imgur.com/BSattXJ.jpg'

        super(Artist, self).save(*args, **kwargs)

    def no_of_songs(self):
        number_of_songs = self.songs.count()
        return number_of_songs

    class Meta:
        ordering = ["name"]

    def __str__(self):
        return self.name
