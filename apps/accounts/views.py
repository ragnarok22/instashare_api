from rest_framework import permissions, viewsets
from rest_framework_simplejwt.views import TokenObtainPairView

from apps.accounts.serializers import UserSerializer, TokenSerializer
from . import models


class UserViewSet(viewsets.ModelViewSet):
    """
    This viewset automatically provides `list`, `create`, `retrieve`,
    `update` and `destroy` actions for **Users**.
    """

    queryset = models.User.objects.all()
    serializer_class = UserSerializer
    permission_classes = [permissions.IsAuthenticatedOrReadOnly]


class TokenView(TokenObtainPairView):
    serializer_class = TokenSerializer
