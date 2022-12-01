from rest_framework import permissions

from apps.accounts.models import User


class IsCreatorOrAdmin(permissions.BasePermission):
    """
    Custom permission to only allow admin or creators of an object to edit it.
    """

    def has_permission(self, request, view):
        if request.user.is_anonymous:
            return False

        return True

    def has_object_permission(self, request, view, obj):
        if request.user.is_superuser:
            return True

        if isinstance(obj, User):
            return obj == request.user

        return obj.creator == request.user
