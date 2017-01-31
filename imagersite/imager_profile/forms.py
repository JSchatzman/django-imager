from django import forms
from imager_profile.models import ImagerProfile


class EditProfileForm(forms.ModelForm):
    """Form to edit a profile."""

    class Meta:
        model = ImagerProfile
        exclude = []
