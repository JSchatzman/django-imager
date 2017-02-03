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


class EditAlbumForm(forms.ModelForm):
    """Form to edit album."""

    class Meta:
        """Define what should be in the form and exclude fields."""

        model = Album
        exclude = [
            'owner',
            'date_uploaded',
            'date_modified',
            'date_published',
        ]
        fields = ['cover_photo', 'title', 'description']
        title = forms.CharField(label='title', max_length=50)
        description = forms.CharField(label='description', max_length=200)


class EditPhotoForm(forms.ModelForm):
    """Form to edit photos."""

    class Meta:
        """Define what should be in the form."""

        model = Photo
        exclude = [
            'photographer',
            'date_uploaded',
            'date_modified',
            'date_published',
        ]
        fields = ['photo', 'title', 'description']
        title = forms.CharField(label='title', max_length=50)
        description = forms.CharField(label='description', max_length=200)
