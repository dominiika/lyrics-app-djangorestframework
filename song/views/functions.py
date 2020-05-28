import requests
from bs4 import BeautifulSoup
import re


def get_lyrics(artist, song):
    artist = re.sub("[^A-Za-z0-9]+", "", artist.lower())
    if artist.startswith("the"):
        artist = artist.replace("the", "", 1)
    song = re.sub("[^A-Za-z0-9]+", "", song.lower())
    r = requests.get(f"https://www.azlyrics.com/lyrics/{artist}/{song}.html")
    c = r.content
    soup = BeautifulSoup(c, "html.parser")
    try:
        lyrics = (
            soup.find("div", {"class": "col-xs-12 col-lg-8 text-center"})
            .find("div", {"class": ""})
            .text
        )
        if lyrics.startswith("\n\r\n"):
            lyrics = lyrics.replace("\n\r\n", "", 1)
        return lyrics
    except AttributeError:
        return None


def get_int_params(queryset):
    return [int(str_id) for str_id in queryset.split(",")]


def artist_filter(queryset, artist):
    try:
        artist_ids = get_int_params(artist)
        queryset = queryset.filter(artist__id__in=artist_ids)
        return queryset
    except:
        pass


def genre_filter(queryset, genre):
    try:
        genre_ids = get_int_params(genre)
        queryset = queryset.filter(genres__id__in=genre_ids)
        return queryset
    except:
        pass


def latest_songs_filter(queryset, latest):
    try:
        queryset = queryset.order_by("-id")[: int(latest)]
        return queryset
    except:
        pass


def highest_rated_filter(queryset, highest):
    try:

        # sort due to the highest rate
        highest_rate = sorted(queryset, key=lambda x: x.avg_rating(), reverse=True)
        # sort due to the highest number of votes
        highest_amount = sorted(queryset, key=lambda x: x.no_of_ratings(), reverse=True)

        # give points based on the index. the less points, the higher rank
        # (because of the lowest indexes of the best songs in highest_rate and highest_amount)
        points = {}
        for i in range(len(highest_rate)):
            points[highest_rate[i]] = i
        for i in range(len(highest_amount)):
            points[highest_amount[i]] += i

        # sort by the number of points to get the result based on the rate and the number of votes.
        # the less points, the better
        queryset = [
            song for song, val in sorted(points.items(), key=lambda item: item[1])
        ][: int(highest)]
        return queryset
    except:
        pass
