from rest_framework import permissions
from django.contrib.auth import logout
from rest_framework import status, viewsets
from rest_framework.response import Response
from rest_framework.views import APIView
from rest_framework_simplejwt.views import TokenObtainPairView

from apps.accounts.models import User
from apps.accounts.permissions import IsCreatorOrAdmin
from apps.accounts.serializers import (
    RegistrationSerializer,
    TokenSerializer,
    UserSerializer,
)


class UserViewSet(viewsets.ModelViewSet):
    serializer_class = UserSerializer
    queryset = User.objects.all()

    def get_permissions(self):
        """
        Instantiates and returns the list of permissions that this view requires.
        """
        if self.action == "list" or self.action == "create":
            permission_classes = [
                permissions.IsAdminUser,
            ]
        else:
            permission_classes = [
                IsCreatorOrAdmin,
            ]
        return [permission() for permission in permission_classes]


class RegistrationView(APIView):
    def post(self, request):
        serializer = RegistrationSerializer(data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data, status=status.HTTP_201_CREATED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)


class LogoutView(APIView):
    def post(self, request):
        logout(request)
        return Response(
            {"message": "Successfully Logged out"}, status=status.HTTP_200_OK
        )


class TokenView(TokenObtainPairView):
    serializer_class = TokenSerializer
