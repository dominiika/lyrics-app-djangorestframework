import uuid
import os
from main.models import SpotifyAPIToken
from main.api.spotify_api import ArtistSpotifyAPI
from django.conf import settings


def artist_image_file_path(instance, filename):
    extension = filename.split(".")[1]
    filename = f"{uuid.uuid4()}.{extension}"

    return os.path.join("upload/artist", filename)


def get_spotify_image(obj):
    spotify_token = SpotifyAPIToken.objects.last()
    spotify_api = ArtistSpotifyAPI(
        settings.SPOTIFY_CLIENT_ID, settings.SPOTIFY_CLIENT_SECRET, spotify_token
    )
    try:
        result = spotify_api.get_artist(obj.name)
        return result
    except:
        return None
