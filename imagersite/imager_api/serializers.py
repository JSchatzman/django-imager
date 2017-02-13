"""Serialization implementation of rest api for photos."""

from rest_framework import serializers
from imager_images.models import Photo, Album


class PhotoSerializer(serializers.HyperlinkedModelSerializer):
    """Serializer for photos."""

    author = serializers.ReadOnlyField(source='author.username')

    class Meta():
        model = Photo
        fields = ('title', 'description', 'published', 'date_uploaded', 'author', 'photo')


class AlbumSerializer(serializers.HyperlinkedModelSerializer):
    """Serializer for albums."""

    photos = PhotoSerializer(many=True)
    owner = serializers.ReadOnlyField(source='owner.user.username')

    class Meta():
        model = Album
        fields = ('owner', 'description', 'published', 'date_uploaded', 'photos')
