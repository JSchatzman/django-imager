"""Url patterns for imager_api."""

from django.conf.urls import url
from rest_framework.urlpatterns import format_suffix_patterns
from imager_api.views import PhotoAPIList


urlpatterns = [
    url(r'^(?P<username>[\w.@+-]+)/$', PhotoAPIList.as_view(), name='photo_list'),
]

