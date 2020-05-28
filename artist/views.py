from rest_framework import viewsets
from rest_framework.authentication import TokenAuthentication
from rest_framework.permissions import IsAuthenticatedOrReadOnly
from main import permissions
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

    def perform_create(self, serializer):
        return serializer.save(user=self.request.user)

    def perform_update(self, serializer):
        return serializer.save(edited_by_user=self.request.user, edited=True)
