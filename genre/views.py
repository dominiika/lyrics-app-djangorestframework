from rest_framework import viewsets
from rest_framework.authentication import TokenAuthentication
from rest_framework.permissions import IsAuthenticatedOrReadOnly
from main import permissions
from .serializers import GenreSerializer
from .models import Genre
from rest_framework.pagination import LimitOffsetPagination


class GenreViewSet(viewsets.ModelViewSet):

    serializer_class = GenreSerializer
    queryset = Genre.objects.all()

    authentication_classes = (TokenAuthentication,)
    permission_classes = (
        IsAuthenticatedOrReadOnly,
        permissions.UpdateOwnModel,
    )

    pagination_class = None

    # enable filters:
    def get_queryset(self):
        # /api/genres/?is_assigned=1
        # returns only assigned genres
        is_assigned = bool(int(self.request.query_params.get("is_assigned", 0)))
        queryset = self.queryset
        if is_assigned:
            queryset = queryset.filter(song__isnull=False)

        if "paginated" in self.request.query_params:
            self.pagination_class = LimitOffsetPagination

        return queryset.distinct()

    def perform_create(self, serializer):
        return serializer.save(user=self.request.user)

    def perform_update(self, serializer):
        return serializer.save(edited_by_user=self.request.user, edited=True)
