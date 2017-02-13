"""Implement security on imager api."""

from rest_framework import permissions


class IsOwnerOrReadOnly(permissions.BasePermission):
    """Customer permissiosn for imager api."""

    def has_object_permission(self, request, view, obj):
        """Only allow get, head and options methods."""
        if request.method in permissions.SAFE_METHODS:
            return True
        return obj.user == request.user
