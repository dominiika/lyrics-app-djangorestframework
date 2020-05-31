from rest_framework import viewsets, status
from rest_framework.authentication import TokenAuthentication
from rest_framework.permissions import IsAuthenticatedOrReadOnly, IsAuthenticated
from main import permissions
from rest_framework.decorators import action
from rest_framework.response import Response
from song.serializers import SongSerializer, SongDetailSerializer, RatingSerializer
from song.models import Song, Rating
from django.contrib.auth import get_user_model
from .functions import (
    get_lyrics,
    artist_filter,
    genre_filter,
    latest_songs_filter,
    highest_rated_filter,
)
from rest_framework.pagination import LimitOffsetPagination
from django.conf import settings


class SongViewSet(viewsets.ModelViewSet):

    serializer_class = SongSerializer

    authentication_classes = (TokenAuthentication,)
    permission_classes = (IsAuthenticatedOrReadOnly, permissions.DeleteOwnModel)
    pagination_class = None

    def get_serializer_class(self):
        if self.action == "retrieve":
            return SongDetailSerializer

        return self.serializer_class

    def get_queryset(self):
        # /api/songs/?genre=3&artist=1

        artist = self.request.query_params.get("artist")
        genre = self.request.query_params.get("genre")

        latest = self.request.query_params.get("latest")
        highest = self.request.query_params.get("highest")

        queryset = Song.objects.all()

        if artist:
            queryset = artist_filter(queryset, artist)
        if genre:
            queryset = genre_filter(queryset, genre)
        if latest:
            queryset = latest_songs_filter(queryset, latest)
        if highest:
            queryset = highest_rated_filter(queryset, highest)

        if "paginated" in self.request.query_params:
            self.pagination_class = LimitOffsetPagination

        return queryset

    @action(detail=True, methods=["POST"])
    def rate(self, request, pk=None):
        if "points" in request.data:
            song = Song.objects.get(id=pk)
            points = request.data["points"]
            user = request.user

            try:
                rating = Rating.objects.get(user=user.id, song=song.id)
                rating.points = points
                rating.save()
                rating_serializer = RatingSerializer(rating, many=False)
                song_serializer = SongDetailSerializer(song, many=False)

                response = {
                    "message": "Rating has been updated",
                    "result": rating_serializer.data,
                    "song": song_serializer.data,
                }
                return Response(response, status=status.HTTP_200_OK)
            except:
                rating = Rating.objects.create(user=user, song=song, points=points)
                rating_serializer = RatingSerializer(rating, many=False)
                song_serializer = SongDetailSerializer(song, many=False)
                response = {
                    "message": "Rating has been created",
                    "result": rating_serializer.data,
                    "song": song_serializer.data,
                }
                return Response(response, status=status.HTTP_201_CREATED)
        else:
            response = {"message": "Points are required."}
            return Response(response, status=status.HTTP_400_BAD_REQUEST)

    @action(detail=False, methods=["POST"])
    def fetch(self, request):
        artist = request.data["artist"]
        title = request.data["title"]
        lyrics = get_lyrics(artist, title, settings.GENIUS_ACCESS_TOKEN)
        response = {"lyrics": lyrics}
        return Response(response, status=status.HTTP_200_OK)

    def perform_create(self, serializer):
        return serializer.save(user=self.request.user)

    def perform_update(self, serializer):
        return serializer.save(
            edited_by_user=self.request.user,
            edited_by_user_str=self.request.user.username,
            edited=True,
        )


class RatingViewSet(viewsets.ModelViewSet):
    queryset = Rating.objects.all()
    serializer_class = RatingSerializer
    authentication_classes = (TokenAuthentication,)
    permission_classes = (IsAuthenticatedOrReadOnly, permissions.DeleteOwnModel)

    @action(detail=False, methods=["POST"], url_path="get-rate")
    def get_rate(self, request):
        if "song" in request.data and "user" in request.data:
            try:
                song_id = int(request.data["song"])
                song = Song.objects.get(pk=song_id)
                user_id = int(request.data["user"])
                user = get_user_model().objects.get(pk=user_id)
                rating = Rating.objects.get(song=song, user=user)
                serializer = RatingSerializer(rating, many=False)
                response = {"result": serializer.data}
                return Response(response, status=status.HTTP_200_OK)
            except:
                response = {"message": "Matching result does not exist."}
                return Response(response, status=status.HTTP_404_NOT_FOUND)
        else:
            response = {"message": "Song and user are required."}
            return Response(response, status=status.HTTP_400_BAD_REQUEST)

    def update(self, request, *args, **kwargs):
        response = {
            "message": f'To update the rating, go to /api/songs/{request.data["song"]}/rate/'
        }
        return Response(response, status=status.HTTP_405_METHOD_NOT_ALLOWED)

    def create(self, request, *args, **kwargs):
        response = {
            "message": f'To rate this song, go to /api/songs/{request.data["song"]}/rate/'
        }
        return Response(response, status=status.HTTP_405_METHOD_NOT_ALLOWED)
