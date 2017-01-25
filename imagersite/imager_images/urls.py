"""Url patterns for imager_images."""

from django.conf.utils import url
from imager_profile.views import all_photos_view, all_albums_view, photo_view, album_view

urlpatterns = [
    url(r'^photos/$', all_photos_view, name="photos"),
    url(r'^photos/(?P<pk>\d+)/$', photo_view, name="photo"),
    url(r'^albums/$', all_albums_view, name="albums"),
    url(r'^albums/(?P<pk>\d+)/$', album_view, name="album")
]
