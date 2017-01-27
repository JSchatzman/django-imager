"""Url patterns for imager_images."""

from django.conf.urls import url
from imager_images.views import (
    AllPhotosView,
    AllAlbumsView,
    PhotoView,
    AlbumView,
    LibraryView,
    AddPhotoView,
    AddAlbumView
)

urlpatterns = [
    url(r'^photos/$', AllPhotosView.as_view(), name="photos"),
    url(r'^photos/(?P<pk>\d+)/$', PhotoView.as_view(), name="photo"),
    url(r'^albums/$', AllAlbumsView.as_view(), name="albums"),
    url(r'^albums/(?P<pk>\d+)/$', AlbumView.as_view(), name="album"),
    url(r'^library/$', LibraryView.as_view(), name="library"),
    url(r'^photos/add/$', AddPhotoView.as_view(), name="add_photo"),
    url(r'^albums/add/$', AddAlbumView.as_view(), name="add_album")
]
