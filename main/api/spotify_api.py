import requests
import base64
from main.models import SpotifyAPIToken
from django.utils import timezone


class SpotifyAPI:
    def __init__(self, client_id, client_secret, token):
        self.client_id = client_id
        self.client_secret = client_secret
        self.token = token

    def _get_base64_credentials(self):
        client_credentials = f"{self.client_id}:{self.client_secret}"
        return base64.b64encode(client_credentials.encode())

    def _check_if_expired(self):
        now = timezone.now()
        if self.token is None:
            return self._create_token()
        elif self.token.expires < now:
            SpotifyAPIToken.objects.last().delete()
            return self._create_token()

    def _create_token(self):
        base64_creds = self._get_base64_credentials()
        response = requests.post(
            "https://accounts.spotify.com/api/token",
            headers={
                "Authorization": f"Basic {base64_creds.decode()}",
                "Content-Type": "application/x-www-form-urlencoded",
            },
            data="grant_type=client_credentials",
        ).json()
        token = response["access_token"]
        expires_in = response["expires_in"]
        now = timezone.now()
        expires = now + timezone.timedelta(seconds=expires_in)

        # create a new token:
        self.token = SpotifyAPIToken.objects.create(token=token, expires=expires)


class ArtistSpotifyAPI(SpotifyAPI):
    def get_artist(self, name):
        self._check_if_expired()
        response = requests.get(
            f"https://api.spotify.com/v1/search?q={name}&type=artist",
            headers={"Authorization": f"Bearer {self.token.token}"},
        ).json()
        try:
            result = response["artists"]["items"][0]["images"][1]["url"]
            return result
        except:
            return None


class SongSpotifyAPI(SpotifyAPI):
    def get_song(self, title, artist):
        self._check_if_expired()
        response = requests.get(
            f"https://api.spotify.com/v1/search?q=track:{title}%20artist:{artist}&type=track",
            headers={"Authorization": f"Bearer {self.token.token}"},
        ).json()

        try:
            result = response["tracks"]["items"][0]
            return {
                "album_name": result["album"]["name"],
                "album_image": result["album"]["images"][1]["url"],
                "song_id": result["id"],
            }
        except:
            return None
