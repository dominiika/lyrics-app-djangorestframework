from rest_framework import viewsets, status
from rest_framework.authentication import TokenAuthentication
from rest_framework.permissions import IsAuthenticatedOrReadOnly
from main import permissions
from rest_framework.decorators import action
from rest_framework.response import Response
from .serializers import CommentSerializer, CommentLikeSerializer
from .models import Comment, CommentLike
from rest_framework.pagination import LimitOffsetPagination


class CommentViewSet(viewsets.ModelViewSet):
    queryset = Comment.objects.all()
    serializer_class = CommentSerializer
    authentication_classes = (TokenAuthentication,)
    permission_classes = (
        IsAuthenticatedOrReadOnly,
        permissions.UpdateOwnModel,
        permissions.DeleteOwnModel,
    )

    pagination_class = None

    def get_queryset(self):
        queryset = self.queryset

        if "paginated" in self.request.query_params:
            self.pagination_class = LimitOffsetPagination

        return queryset.distinct()

    @action(detail=True, methods=["POST"])
    def like(self, request, pk=None):

        comment = Comment.objects.get(id=pk)
        user = request.user

        try:
            like = CommentLike.objects.get(user=user, comment=comment)
            like.delete()
            response = {"message": "The comment has been disliked."}
            return Response(response, status=status.HTTP_204_NO_CONTENT)
        except:
            CommentLike.objects.create(user=user, comment=comment)
            response = {"message": "The comment has been liked."}
            return Response(response, status=status.HTTP_200_OK)

    def perform_create(self, serializer):
        return serializer.save(user=self.request.user)

    def perform_update(self, serializer):
        return serializer.save(edited=True)


class CommentLikeViewSet(viewsets.ModelViewSet):
    queryset = CommentLike.objects.all()
    serializer_class = CommentLikeSerializer
    authentication_classes = (TokenAuthentication,)
    permission_classes = (IsAuthenticatedOrReadOnly,)

    pagination_class = None

    def get_queryset(self):
        queryset = self.queryset

        if "paginated" in self.request.query_params:
            self.pagination_class = LimitOffsetPagination

        return queryset.distinct()

    def update(self, request, *args, **kwargs):
        response = {"message": "Method not allowed"}
        return Response(response, status=status.HTTP_405_METHOD_NOT_ALLOWED)

    def create(self, request, *args, **kwargs):
        response = {"message": "Method not allowed"}
        return Response(response, status=status.HTTP_405_METHOD_NOT_ALLOWED)
