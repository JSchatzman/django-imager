from django.shortcuts import render
from imager_images.models import Photo, Album
from django.views.generic import TemplateView


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


def photo_view(request, pk):
    """View a photo."""
    photo = Photo.objects.get(pk=pk)
    return render(request, 'imager_images/photo_id.html', {'photo': photo})


def album_view(request, pk):
    """View a album."""
    album = Album.objects.get(pk=pk)
    photos = album.photos.all()
    return render(request, 'imager_images/album_id.html', {"album": album, "photos": photos})


def all_photos_view(request):
    """View all photos."""
    photos = Photo.objects.filter(published='Public').all()
    return render(request, 'imager_images/all_photos.html', {'photos': photos})


def all_albums_view(request):
    """View all albums."""
    albums = Album.objects.filter(published='Public').all()
    return render(request, 'imager_images/all_albums.html', {'albums': albums})


def library_view(request):
    """View for library page."""
    if request.user.is_authenticated():
        albums = request.user.profile.albums.all()
        photos = request.user.profile.photos.all()
        return render(request, "imager_images/library.html", {
            'albums': albums,
            'photos': photos})
