from django.shortcuts import render
from imager_images.models import Photo, Album
from django.views.generic import TemplateView

from django.shortcuts import redirect


class PhotoView(TemplateView):
    """Class based view for a Photo."""

    template_name = "imager_images/photo_id.html"

    def get_context_data(self, pk):
        """Rewrite get_context_data to add our data."""
        photo = Photo.objects.get(pk=pk)
        if photo.published == 'PUBLIC' or photo.photographer.user == self.request.user:
            return {'photo': photo}
        else:
            error = "You cannot view this photo because Kam Chancellor hit you in face."
            return {"error": error}


class AlbumView(TemplateView):
    """View a album."""

    template_name = 'imager_images/album_id.html'

    def get_context_data(self, pk):
        """Get context for album view."""
        album = Album.objects.get(pk=pk)
        photos = album.photos.all()
        return {"album": album, "photos": photos}


class AllPhotosView(TemplateView):
    """View all photos."""

    template_name = 'imager_images/all_photos.html'

    def get_context_data(self):
        """Get context for all photos view."""
        photos = Photo.objects.filter(published='Public').all()
        return {'photos': photos}


class AllAlbumsView(TemplateView):
    """View all albums."""

    template_name = 'imager_images/all_albums.html'

    def get_context_data(self):
        """Get context for all albums view."""
        albums = Album.objects.filter(published='Public').all()
        return {'albums': albums}


class LibraryView(TemplateView):
    """View for library page."""

    template_name = 'imager_images/library.html'

    def get_context_data(self):
        """Get context for library view."""
        if self.request.user.is_authenticated():
            albums = self.request.user.profile.albums.all()
            photos = self.request.user.profile.photos.all()
            return {'albums': albums, 'photos': photos}
