from django import forms
from imager_profile.models import ImagerProfile


class EditProfileForm(forms.ModelForm):
    """Form to edit a profile."""

    def __init__(self, *args, **kwargs):
        """Form."""
        super(EditProfileForm, self).__init__(*args, **kwargs)
        self.fields["name"] = forms.CharField(initial=self.instance.user.first_name)
        self.fields["camera_type"] = forms.CharField(initial=self.instance.user.profile.camera_type)
        self.fields["personal_website"] = forms.URLField(initial=self.instance.user.profile.personal_website)
        self.fields["bio"] = forms.CharField(initial=self.instance.user.profile.bio)
        self.fields["travel_radius"] = forms.DecimalField(initial=self.instance.user.profile.travel_radius)
        self.fields["phone"] = forms.CharField(initial=self.instance.user.profile.phone)
        self.fields["photo_type"] = forms.CharField(initial=self.instance.user.profile.photo_type)
        del self.fields["user"]

    class Meta:
        model = ImagerProfile
        exclude = []
