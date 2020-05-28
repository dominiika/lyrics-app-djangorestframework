from rest_framework import viewsets
from user.permissions import UpdateOwnProfile
from .serializers import UserSerializer
from rest_framework.authtoken.views import ObtainAuthToken
from django.contrib.auth import get_user_model
from rest_framework.authentication import TokenAuthentication

from rest_framework.authtoken.models import Token
from rest_framework.response import Response


class UserViewSet(viewsets.ModelViewSet):
    serializer_class = UserSerializer
    queryset = get_user_model().objects.all()

    authentication_classes = (TokenAuthentication,)
    permission_classes = (UpdateOwnProfile,)


class CreateTokenViewSet(ObtainAuthToken):
    def post(self, request, *args, **kwargs):
        serializer = self.serializer_class(
            data=request.data, context={"request": request}
        )
        serializer.is_valid(raise_exception=True)
        user = serializer.validated_data["user"]
        token, created = Token.objects.get_or_create(user=user)
        return Response(
            {
                "token": token.key,
                "user": user.pk,
                "username": user.username,
                "email": user.email,
            }
        )
