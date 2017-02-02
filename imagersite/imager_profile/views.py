"""Implementation of profile views."""

from django.contrib.auth.models import User
from imager_images.models import Photo, Album
from django.views.generic import TemplateView, UpdateView
from imager_profile.forms import EditProfileForm
from imager_profile.models import ImagerProfile
from django.http import HttpResponseRedirect
from django.urls import reverse_lazy
from django.contrib.auth.mixins import LoginRequiredMixin
from django.db.models.signals import pre_save


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
            'public_albums': albums.filter(published='PUBLIC'),
            'private_albums': albums.filter(published='PRIVATE'),
            'photo_count': len(photos),
            'album_count': len(albums)
        }
        return {'user_profile': user_profile, 'data': data}


class EditProfileView(LoginRequiredMixin, UpdateView):
    """Edit the authenticated users profile."""

    login_required = True
    template_name = 'imager_profile/edit_profile_form.html'
    form_class = EditProfileForm
    model = ImagerProfile

    def get_object(self):
        """Get the user profile object."""
        return self.request.user.profile

    def form_valid(self, form):
        """Save model forms to database."""
        self.object = form.save()
        self.object.user.first_name = form.cleaned_data['name']
        self.object.user.profile.camera_type = form['camera_type']
        self.object.user.profile.personal_website = form['personal_website']
        self.object.user.profile.bio = form['bio']
        self.object.user.profile.traversal_radius = form['travel_radius']
        self.object.user.profile.phone = form['phone']
        self.object.user.profile.photo_type = form['photo_type']
        self.object.user.save()
        self.object.save()
        return HttpResponseRedirect('profile')