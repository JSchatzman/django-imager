from django.shortcuts import render
from imager_images.models import Photo, Album

# Create your views here.


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
