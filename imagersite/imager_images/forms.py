from django import forms
from imager_images.models import Photo, Album


class AddPhotoForm(forms.ModelForm):

    class Meta:
        model = Photo
        exclude = ['photographer', 'date_modified', 'date_published', 'date_uploaded']