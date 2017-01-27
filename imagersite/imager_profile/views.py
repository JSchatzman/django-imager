from django.shortcuts import render
from django.contrib.auth.models import User
from imager_images.models import Photo, Album
from django.views.generic import TemplateView


# Create your views here.
class HomeView(TemplateView):
    """View for the home page."""
    template_name = 'imagersite/home.html'

    def get_context_data(self, name=''):
        """Get context for home view."""
        return {'name': name}


def profile_view(request, username=None):
    """View for profile page."""
    if not username:
        username = request.user.username
    user_profile = User.objects.get(username=username).profile
    #import pdb; pdb.set_trace()
    photos = Photo.objects.all().filter(photographer=user_profile.user_id)
    albums = Album.objects.all().filter(owner=user_profile)
    data = {
        'public_photos': photos.filter(published='PUBLIC'),
        'private_photos': photos.filter(published='PRIVATE'),
        'shared_photos': photos.filter(published='SHARED'),
        'photo_count': len(photos),
        'album_count': len(albums)
    }
    return render(request,
                  '../templates/profile.html',
                 {'user_profile': user_profile, 'data': data})
