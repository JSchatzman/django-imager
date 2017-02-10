from django.shortcuts import render
from imager_images.models import Photo, Album
from imager_images.forms import AddPhotoForm, AddAlbumForm, EditPhotoForm, EditAlbumForm
from django.views.generic import TemplateView, CreateView, ListView, UpdateView
from django.urls import reverse_lazy
from django.contrib.auth.mixins import LoginRequiredMixin
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
            error = "You cannot view this photo because you are not logged in."
            return {"error": error}


class AlbumView(TemplateView):
    """View a album."""

    template_name = 'imager_images/album_id.html'

    def get_context_data(self, pk):
        """Get context for album view."""
        album = Album.objects.get(pk=pk)
        photos = album.photos.all()
      #  import pdb; pdb.set_trace()
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
        return Album.objects.filter(owner=self.request.user.profile)


class LibraryView(TemplateView):
    """View for library page."""

    template_name = 'imager_images/library.html'

    def get_context_data(self):
        """Get context for library view."""
        if self.request.user.is_authenticated():
            albums = self.request.user.profile.albums.all()
            photos = self.request.user.profile.photos.all()
            user = self.request.user
            return {'albums': albums, 'photos': photos, 'user': user}


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
    login_required = True
    form_class = AddAlbumForm
    template_name = 'imager_images/add_album.html'

    def get_form(self):
        """Make some alterations to default get_form method."""
        form = super(AddAlbumView, self).get_form()
        form.fields['cover_photo'].queryset = self.request.user.profile.photos.all()
        form.fields['photos'].queryset = self.request.user.profile.photos.all()
        return form

    def form_valid(self, form):
        album = form.save()
        album.owner = self.request.user.profile
        album.date_uploaded = timezone.now()
        album.date_modified = timezone.now()
        if album.published == "PUBLIC":
            album.published_date = timezone.now()
        album.save()
        return redirect('library')



class EditPhotoView(LoginRequiredMixin, UpdateView):
    """Edit a photo."""

    login_required = True
    template_name = 'imager_images/edit_photo_form.html'
    success_url = reverse_lazy('library')
    form_class = EditPhotoForm
    model = Photo

    def direct(self, request, *args, **kwargs):
        """Forbid users who do not own the photo."""
        if not self.check_user(request):
            return HttpResponseForbidden()
        return super(EditPhotoView, self).direct(request, *args, **kwargs)

    def check_user(self, request):
        """User is the owner of picture.."""
        if request.user.is_authenticated():
            self.object = self.get_object()
            return self.object.photographer.user == request.user
        return False



class EditAlbumView(LoginRequiredMixin, UpdateView):
    """Edit an album."""

    login_required = True
    template_name = 'imager_images/edit_album_form.html'
    success_url = reverse_lazy('library')
    form_class = EditAlbumForm
    model = Album

    def get_form(self):
        """Make some alterations to default get_form method."""
        form = super(EditAlbumView, self).get_form()
        form.fields['cover_photo'].queryset = self.request.user.profile.photos.all()
        form.fields['photos'].queryset = self.request.user.profile.photos.all()
        return form
        
    def direct(self, request, *args, **kwargs):
        """Forbid users who do not own the album."""
        if not self.check_user(request):
            return HttpResponseForbidden()
        return super(EditAlbumView, self).direct(request, *args, **kwargs)

    def check_user(self, request):
        """User is owner of album."""
        if request.user.is_authenticated():
            self.object = self.get_object()
            return self.object.owner.user == request.user
        return False
