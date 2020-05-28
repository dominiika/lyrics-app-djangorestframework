from django.urls import path, include
from . import views
from rest_framework.routers import DefaultRouter

app_name = "user"

router = DefaultRouter()
router.register("users", views.UserViewSet, basename="users")


urlpatterns = [
    path("", include(router.urls)),
    path("token/", views.CreateTokenViewSet.as_view(), name="token"),
]
