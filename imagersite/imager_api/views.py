"""Views for images api."""
from django.contrib.auth.models import User
from imager_api.serializers import PhotoSerializer
from imager_images.models import Photo
from rest_framework import mixins
from rest_framework import generics
from imager_api.permissions import IsOwnerOrReadOnly
from rest_framework import permissions


class PhotoAPIList(mixins.ListModelMixin,
                   generics.GenericAPIView):
    """Implementation of photo list api."""

    serializer_class = PhotoSerializer
    permission_classes = (permissions.IsAuthenticatedOrReadOnly,
                          IsOwnerOrReadOnly)

    def get_queryset(self):
        """Rewrite queryset to provide list of photos for single user."""
        user = User.objects.get(username=self.kwargs['username'])
        if user == self.request.user:
            photos = user.profile.photos.all()
        else:
            photos = user.profile.photos.filter(published="PUBLIC")
        return photos

    def get(self, request, *args, **kwargs):
        return self.list(request, *args, **kwargs)
