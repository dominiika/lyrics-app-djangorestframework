from django.core.management.utils import get_random_secret_key
import os
from .base import BASE_DIR

DEBUG = True

ALLOWED_HOSTS = []

try:
    from lyricsapp.settings.secret_key import SECRET_KEY
except ImportError:
    SETTINGS_DIR = os.path.abspath(os.path.dirname(__file__))
    with open(os.path.join(SETTINGS_DIR, 'secret_key.py'), 'w') as file:
        file.write(f'SECRET_KEY="{get_random_secret_key()}"')
    from lyricsapp.settings.secret_key import SECRET_KEY


CORS_ORIGIN_ALLOW_ALL = True


DATABASES = {
    'default': {
        'ENGINE': 'django.db.backends.sqlite3',
        'NAME': os.path.join(BASE_DIR, 'db.sqlite3'),
    }
}

# # uncomment it and provide your credentials:
# SPOTIFY_CLIENT_ID = 'your Spotify client ID'
# SPOTIFY_CLIENT_SECRET = 'your Spotify client secret'
# YOUTUBE_API_KEY = 'your YT client key'
