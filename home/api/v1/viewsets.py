from rest_framework.authtoken.serializers import AuthTokenSerializer
from rest_framework.viewsets import ModelViewSet, ViewSet
from rest_framework.authtoken.models import Token
from rest_framework.response import Response
from rest_framework import authentication, permissions

from home.api.v1.serializers import (
    SignupSerializer,
    UserSerializer,
)
from users.models import User


class SignupViewSet(ModelViewSet):
    permission_classes = [permissions.AllowAny, ]
    authentication_classes = []
    serializer_class = SignupSerializer
    http_method_names = ["post"]

    def create(self, request, *args, **kwargs):
        serializer = SignupSerializer(data=request.data)
        if serializer.is_valid(raise_exception=True):
            data = serializer.save()
            #user = User.objects.get(id=data.id)
            token, created = Token.objects.get_or_create(user=data)
            user_serializer = UserSerializer(data)
            return Response({"token": token.key, "user": user_serializer.data})
        return Response(serializer.errors)


class LoginViewSet(ViewSet):
    """Based on rest_framework.authtoken.views.ObtainAuthToken"""
    authentication_classes = []
    permission_classes = [permissions.AllowAny, ]
    serializer_class = AuthTokenSerializer

    def create(self, request):
        serializer = self.serializer_class(
            data=request.data, context={"request": request}
        )
        serializer.is_valid(raise_exception=True)
        user = serializer.validated_data["user"]
        token, created = Token.objects.get_or_create(user=user)
        user_serializer = UserSerializer(user)
        return Response({"token": token.key, "user": user_serializer.data})
