"""Url patterns for imager profile."""

from django.conf.urls import url
from imager_profile.views import ProfileView, EditProfileView


urlpatterns = [
    url(r'^$', ProfileView.as_view(), name='my_profile'),
    url(r'^(?P<username>\w+)/$', ProfileView.as_view(), name='profile'),
    url(r'^(?P<username>\w+)/edit/$', EditProfileView.as_view(), name='edit_profile'),
]
