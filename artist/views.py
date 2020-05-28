from rest_framework import viewsets, status
from rest_framework.authentication import TokenAuthentication
from rest_framework.permissions import IsAuthenticatedOrReadOnly, IsAuthenticated
from main import permissions
from rest_framework.decorators import action
from rest_framework.response import Response
from .serializers import ArtistSerializer, ArtistImageSerializer
from .models import Artist
from rest_framework.pagination import LimitOffsetPagination


class ArtistViewSet(viewsets.ModelViewSet):

    serializer_class = ArtistSerializer
    queryset = Artist.objects.all()

    authentication_classes = (TokenAuthentication,)
    permission_classes = (IsAuthenticatedOrReadOnly, permissions.UpdateOwnModel)

    pagination_class = None

    def get_serializer_class(self):
        if self.action == "upload_image":
            return ArtistImageSerializer

        return self.serializer_class

    # enable filters:
    def get_queryset(self):
        # /api/artists/?is_assigned=1
        # returns only assigned artists
        is_assigned = bool(int(self.request.query_params.get("is_assigned", 0)))
        queryset = Artist.objects.all()
        songs_no = self.request.query_params.get("highest_number_of_songs")
        if is_assigned:
            queryset = queryset.filter(songs__isnull=False).distinct()

        if songs_no:
            try:
                queryset = sorted(
                    queryset, key=lambda x: x.no_of_songs(), reverse=True
                )[: int(songs_no)]
            except:
                pass

        if "paginated" in self.request.query_params:
            self.pagination_class = LimitOffsetPagination

        return queryset

    @action(methods=["POST"], detail=True, url_path="upload-image")
    def upload_image(self, request, pk=None):
        artist = self.get_object()
        serializer = self.get_serializer(artist, data=request.data)

        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data, status=status.HTTP_200_OK)

        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

    def perform_create(self, serializer):
        return serializer.save(user=self.request.user)

    def perform_update(self, serializer):
        return serializer.save(edited_by_user=self.request.user, edited=True)
