from django.db import models


class SpotifyAPIToken(models.Model):
    token = models.CharField(max_length=255)
    expires = models.DateTimeField(blank=True)
