from django.urls import path, include
from genre.views import GenreViewSet
from artist.views import ArtistViewSet
from song.views import SongViewSet
from song.views import RatingViewSet
from comment.views import CommentViewSet
from comment.views import CommentLikeViewSet

from rest_framework.routers import DefaultRouter

app_name = "main"

router = DefaultRouter()
router.register("genres", GenreViewSet, basename="genres")
router.register("artists", ArtistViewSet, basename="artists")
router.register("songs", SongViewSet, basename="songs")
router.register("ratings", RatingViewSet, basename="ratings")
router.register("comments", CommentViewSet, basename="comments")
router.register("comment_likes", CommentLikeViewSet, basename="comment_likes")


urlpatterns = [
    path("", include(router.urls)),
]
