from django import forms
from imager_profile.models import ImagerProfile


class EditProfileForm(forms.ModelForm):
    """Form to edit a profile."""

    def __init__(self, *args, **kwargs):
        """Form."""
        super(EditProfileForm, self).__init__(*args, **kwargs)
        self.fields["hireable"] = forms.BooleanField(initial=self.instance.user.profile.hireable)
        self.fields["camera_type"] = forms.CharField(initial=self.instance.user.profile.camera_type)
        self.fields["personal_website"] = forms.URLField(initial=self.instance.user.profile.personal_website)
        self.fields["bio"] = forms.CharField(initial=self.instance.user.profile.bio)
        self.fields["travel_radius"] = forms.IntegerField(initial=self.instance.user.profile.travel_radius)
        self.fields["phone"] = forms.RegexField(regex=r'^\+?1?\d{9,15}$', error_message="Plese enter a phone number", initial=self.instance.user.profile.phone)
        self.fields["photo_type"] = forms.CharField(initial=self.instance.user.profile.photo_type)
        del self.fields["user"]

    class Meta:
        model = ImagerProfile
        exclude = []
