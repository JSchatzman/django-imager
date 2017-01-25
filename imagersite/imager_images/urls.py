"""Url patterns for imager_images."""

from django.conf.urls import url
from imager_images.views import all_photos_view, all_albums_view, photo_view, album_view, library_view

urlpatterns = [
    url(r'^photos/$', all_photos_view, name="photos"),
    url(r'^photos/(?P<pk>\d+)/$', photo_view, name="photo"),
    url(r'^albums/$', all_albums_view, name="albums"),
    url(r'^albums/(?P<pk>\d+)/$', album_view, name="album"),
    url(r'^library/$', library_view, name="library")
]