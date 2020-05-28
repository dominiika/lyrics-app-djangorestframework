from main.models import SpotifyAPIToken
from main.api.spotify_api import SongSpotifyAPI
from main.api.youtube_api import YoutubeAPI
from django.conf import settings


def get_number_of_items(items):
    return items.count()


def get_spotify_data(obj):
    spotify_token = SpotifyAPIToken.objects.last()
    spotify_api = SongSpotifyAPI(
        settings.SPOTIFY_CLIENT_ID, settings.SPOTIFY_CLIENT_SECRET, spotify_token
    )
    try:
        return spotify_api.get_song(obj.title, obj.artist.name)
    except:
        return None


def save_spotify_song_id(obj):
    try:
        return get_spotify_data(obj)["song_id"]
    except:
        pass


def save_spotify_album_name(obj):
    try:
        return get_spotify_data(obj)["album_name"]
    except:
        pass


def save_spotify_album_image(obj):
    try:
        return get_spotify_data(obj)["album_image"]
    except:
        pass


def get_youtube_data(self):
    youtube_api = YoutubeAPI(settings.YOUTUBE_API_KEY)
    try:
        return youtube_api.get_video_url(self.title, self.artist)
    except:
        return None
