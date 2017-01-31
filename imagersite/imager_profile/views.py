"""Implementation of profile views."""

from django.contrib.auth.models import User
from imager_images.models import Photo, Album
from django.views.generic import TemplateView, UpdateView
from imager_profile.forms import EditProfileForm
from imager_profile.models import ImagerProfile
from django.http import HttpResponseRedirect
from django.urls import reverse_lazy


class HomeView(TemplateView):
    """View for the home page."""

    template_name = 'imagersite/home.html'

    def get_context_data(self, name=''):
        """Get context for home view."""
        return {'name': name}


class ProfileView(TemplateView):
    """Class implementation of profile view."""

    template_name = '../templates/profile.html'

    def get_context_data(self, username=None):
        """View for profile page."""
        if not username:
            username = self.request.user.username
        user_profile = User.objects.get(username=username).profile
        photos = Photo.objects.all().filter(photographer=user_profile.user_id)
        albums = Album.objects.all().filter(owner=user_profile)
        data = {
            'public_photos': photos.filter(published='PUBLIC'),
            'private_photos': photos.filter(published='PRIVATE'),
            'shared_photos': photos.filter(published='SHARED'),
            'photo_count': len(photos),
            'album_count': len(albums)
        }
        return {'user_profile': user_profile, 'data': data}


class EditProfileView(UpdateView):
    """Update profile."""

    login_required = True
    template_name = '../templates/eidt_profile_form.html'
    success_url = reverse_lazy('profile')
    form_class = EditProfileForm
    model = ImagerProfile

    def get_object(self):
        """Define what profile to edit."""
        return self.request.user.profile

    def form_valid(self, form):
        """If form post is successful, set the object's owner."""
        self.object = form.save()
        self.object.user.first_name = form.cleaned_data['First Name']
        self.object.user.last_name = form.cleaned_data['Last Name']
        self.object.user.email = form.cleaned_data['Email']
        self.object.user.save()
        self.object.save()
        return HttpResponseRedirect(self.get_success_url())
