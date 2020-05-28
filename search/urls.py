from django.urls import path, include
from .views import (
    GenreSearchViewSet,
    ArtistSearchViewSet,
    SongSearchViewSet,
    SearchAllViewSet,
)
from rest_framework.routers import DefaultRouter

app_name = "search"

router = DefaultRouter()
router.register("genre", GenreSearchViewSet, basename="search-genre")
router.register("artist", ArtistSearchViewSet, basename="search-artist")
router.register("song", SongSearchViewSet, basename="search-song")


urlpatterns = [
    path("", include(router.urls)),
    path("all/", SearchAllViewSet.as_view(), name="search-all"),
]
