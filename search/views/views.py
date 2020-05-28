from rest_framework.viewsets import ReadOnlyModelViewSet
from rest_framework.response import Response
from rest_framework.views import APIView
from genre.models import Genre
from genre.serializers import GenreSerializer
from artist.models import Artist
from artist.serializers import ArtistSerializer
from song.models import Song
from song.serializers import SongSerializer
from rest_framework.pagination import LimitOffsetPagination
from django.core.paginator import PageNotAnInteger
from rest_framework import status
from .functions import PaginatedSerializer


class SearchAllViewSet(APIView, LimitOffsetPagination):
    def get(self, request, format=None, **kwargs):
        try:
            value = self.request.query_params.get("value")

            genres = Genre.objects.filter(name__icontains=value)
            artists = Artist.objects.filter(name__icontains=value)
            songs = Song.objects.filter(title__icontains=value)

            for genre in genres:
                songs |= Song.objects.filter(genres=genre)
                artists |= Artist.objects.filter(genres=genre)

            # /api/search/all/?value=rock&page_number=1
            page_size = self.request.query_params.get("page_size ", 5)
            page_number = self.request.query_params.get("page_number")

            genre_paginated = PaginatedSerializer(
                genres, GenreSerializer, page_size, page_number
            )
            genre_paginated.get_paginated_serializer()
            artist_paginated = PaginatedSerializer(
                artists, ArtistSerializer, page_size, page_number
            )
            artist_paginated.get_paginated_serializer()
            song_paginated = PaginatedSerializer(
                songs, SongSerializer, page_size, page_number
            )
            song_paginated.get_paginated_serializer()

            no_of_pages = max(
                genre_paginated.num_pages,
                artist_paginated.num_pages,
                song_paginated.num_pages,
            )
            return Response(
                {
                    "number_of_pages": no_of_pages,
                    "number_of_genre_pages": genre_paginated.num_pages,
                    "genres": genre_paginated.paginated_serializer.data,
                    "number_of_artist_pages": artist_paginated.num_pages,
                    "artists": artist_paginated.paginated_serializer.data,
                    "number_of_song_pages": song_paginated.num_pages,
                    "songs": song_paginated.paginated_serializer.data,
                }
            )

        except ValueError:
            return Response(
                {
                    "message": "You've entered a wrong query parameter. "
                    "Type /api/search/all/?value=[your search]&page_number=[page number]/",
                },
                status=status.HTTP_400_BAD_REQUEST,
            )
        except PageNotAnInteger:
            return Response(
                {
                    "message": "You need to add '&page_number=[page number]' to the query."
                },
                status=status.HTTP_400_BAD_REQUEST,
            )


class GenreSearchViewSet(ReadOnlyModelViewSet):
    serializer_class = GenreSerializer

    def get_queryset(self):
        queryset = []
        genres = Genre.objects.all()
        name = self.request.query_params.get("name")
        index = self.request.query_params.get("id")
        if name:
            queryset = genres.filter(name__icontains=name)
        if index:
            queryset = genres.filter(pk__exact=int(index))

        return queryset


class ArtistSearchViewSet(ReadOnlyModelViewSet):
    serializer_class = ArtistSerializer

    def get_queryset(self):
        queryset = []
        artists = Artist.objects.all()
        name = self.request.query_params.get("name")
        index = self.request.query_params.get("id")
        if name:
            queryset = artists.filter(name__icontains=name)
        if index:
            queryset = artists.filter(pk__exact=int(index))

        return queryset


class SongSearchViewSet(ReadOnlyModelViewSet):
    serializer_class = SongSerializer

    def get_queryset(self):
        queryset = []
        songs = Song.objects.all()
        title = self.request.query_params.get("title")
        index = self.request.query_params.get("id")

        if title:
            queryset = songs.filter(title__icontains=title)
        if index:
            queryset = songs.filter(pk__exact=int(index))

        return queryset
