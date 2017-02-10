"""Serialization implementation of rest api for photos."""

from rest_framework import serializers
from imager_images.models import Photo


class PhotoSerializer(serializers.HyperlinkedModelSerializer):
    """Serializer for photos."""

   # import pdb; pdb.set_trace()
    author = serializers.ReadOnlyField(source='author.username')

    class Meta():
        model = Photo
        fields = ('title', 'description', 'published', 'date_uploaded', 'author')
