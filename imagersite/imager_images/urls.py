"""Url patterns for imager_images."""

from django.conf.urls import url
from imager_images.views import AllPhotosView, AllAlbumsView, PhotoView, AlbumView, LibraryView

urlpatterns = [
    url(r'^photos/$', AllPhotosView.as_view(template_name='imager_images/all_photos.html'), name="photos"),
    url(r'^photos/(?P<pk>\d+)/$', PhotoView.as_view(template_name='imager_images/photo_id.html'), name="photo"),
    url(r'^albums/$', AllAlbumsView.as_view(template_name='imager_images/all_albums.html'), name="albums"),
    url(r'^albums/(?P<pk>\d+)/$', AlbumView.as_view(template_name='imager_images/album_id.html'), name="album"),
    url(r'^library/$', LibraryView.as_view(template_name='imager_images/library.html'), name="library")
]
