"""Views for images api."""
from django.contrib.auth.models import User
from imager_api.serializers import PhotoSerializer
from imager_images.models import Photo
from rest_framework import mixins
from rest_framework import generics


class PhotoAPIDetail(generics.GenericAPIView):
    """Implementation of photo detail api."""

    queryset = Photo.objects.all()
    serializer_class = PhotoSerializer


class PhotoAPIList(mixins.ListModelMixin,
                   generics.GenericAPIView):
    """Implementation of photo list api."""

    serializer_class = PhotoSerializer

    def get_queryset(self):
        """Rewrite queryset to provide list of photos for single user."""
        user = User.objects.get(username=self.kwargs['username'])
        photos = user.profile.photos.filter(published="PUBLIC")
        #import pdb; pdb.set_trace()

        return photos

    def get(self, request, *args, **kwargs):
        return self.list(request, *args, **kwargs)
