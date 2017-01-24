from django.shortcuts import render
from django.contrib.auth.models import User
from imager_images.models import Photo, Album

# Create your views here.
def home_view(request, name=''):
    """View for the home page."""
    return render(request, 'imagersite/home.html', context={'name': name})


def profile_view(request, username=None):
    """View for profile page."""
    if not username:
        username = request.user.username
    user_profile = User.objects.get(username=username).profile
    photos = Photo.objects.get(photgrapher=user_profile)
    albums = Album.objects.get(owner=user_profile)
    data = {
    'public_photos' : photos.filter(PUBLISH_TYPE='PUBLIC')
    'private_photos' : photos.filter(PUBLISH_TYPE='PRIVATE')
    'shared_photos' : photos.filter(PUBLISH_TYPE='SHARED')
            }
    return render(request, 
                  template_name,
                  {'profile': user_profile,
                   data : data}