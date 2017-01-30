from django import forms
from imager_images.models import Photo, Album


class AddPhotoForm(forms.ModelForm):
    """Create a photo form."""

    class Meta:
        model = Photo
        exclude = ['photographer', 'date_modified', 'date_published', 'date_uploaded']


class AddAlbumForm(forms.ModelForm):
    """Create an album form."""

    class Meta:
        model = Album
        exclude = ['owner', 'date_modified', 'date_published', 'date_created', 'photos']
