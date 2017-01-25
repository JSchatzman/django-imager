from django.shortcuts import render
from imager_images.models import Photo, Album


def library_view(request):
    """View for library page."""
    if request.user.is_authenticated():
        albums = request.user.profile.albums.all()
        photos = request.user.profile.photos.all()
        return render(request, "imager_images/library.html", {
            'albums': albums,
            'photos': photos})
