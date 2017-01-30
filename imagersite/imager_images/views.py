from django.shortcuts import render
from imager_images.models import Photo, Album
from imager_images.forms import AddPhotoForm, AddAlbumForm
from django.views.generic import TemplateView, CreateView, ListView

from django.shortcuts import redirect
from django.utils import timezone


class PhotoView(TemplateView):
    """Class based view for a Photo."""

    template_name = "imager_images/photo_id.html"

    def get_context_data(self, pk):
        """Rewrite get_context_data to add our data."""
        photo = Photo.objects.get(pk=pk)
        if photo.published == 'PUBLIC' or photo.photographer.user == self.request.user:
            return {'photo': photo}
        else:
            error = "You cannot view this photo because Kam Chancellor laid the boom."
            return {"error": error}


class AlbumView(TemplateView):
    """View a album."""

    template_name = 'imager_images/album_id.html'

    def get_context_data(self, pk):
        """Get context for album view."""
        album = Album.objects.get(pk=pk)
        photos = album.photos.all()
        return {"album": album, "photos": photos}


class AllPhotosView(ListView):
    """View all plbums."""

    template_name = 'imager_images/all_photos.html'
    model = Photo
    context_object_name = "photos"

    def get_queryset(self):
        """Return list of all photos for this user."""
        return Photo.objects.filter(photographer=self.request.user.profile)


class AllAlbumsView(ListView):
    """View all albums."""

    template_name = 'imager_images/all_albums.html'
    model = Album
    context_object_name = "albums"

    def get_queryset(self):
        """Return list of all albums for this user."""
        # import pdb; pdb.set_trace()
        return Album.objects.filter(owner=self.request.user.profile)


class LibraryView(TemplateView):
    """View for library page."""

    template_name = 'imager_images/library.html'

    def get_context_data(self):
        """Get context for library view."""
        if self.request.user.is_authenticated():
            albums = self.request.user.profile.albums.all()
            photos = self.request.user.profile.photos.all()
            return {'albums': albums, 'photos': photos}


class AddPhotoView(CreateView):
    """Class based view for creating photos."""

    model = Photo
    form_class = AddPhotoForm
    template_name = 'imager_images/add_photo.html'

    def form_valid(self, form):
        photo = form.save()
        photo.photographer = self.request.user.profile
        photo.date_uploaded = timezone.now()
        photo.date_modified = timezone.now()
        if photo.published == "PUBLIC":
            photo.published_date = timezone.now()
        photo.save()
        return redirect('library')


class AddAlbumView(CreateView):
    """Class based view for creating photos."""

    model = Album
    form_class = AddAlbumForm
    template_name = 'imager_images/add_album.html'

    def form_valid(self, form):
        album = form.save()
        album.owner = self.request.user.profile
        album.date_uploaded = timezone.now()
        album.date_modified = timezone.now()
        if album.published == "PUBLIC":
            album.published_date = timezone.now()
        album.save()
        return redirect('library')
