"""Implementation of photo and album models."""


from django.db import models
from imager_profile.models import ImagerProfile


PUBLISH_TYPE = (
    ('PRIVATE', 'Private'),
    ('SHARED', 'Shared'),
    ('PUBLIC', 'Public')
)


class Photo(models.model):
    """Model for photo."""

    photo = models.ImageField(upload_to='', blank=True, null=True)
    title = models.CharField(max_length=255, blank=True, null=True)
    description = models.CharField(max_length=255, blank=True, null=True)
    date_published = models.DateField(blank=True, null=True)
    date_uploaded = models.DateField(auto_now=True)
    date_modified = models.DateField(auto_now=True)
    published = models.CharField(max_length=255,
                                 choice=PUBLISH_TYPE,
                                 blank=True,
                                 null=True)
    phototographer = models.ForeignKey(ImagerProfile,
                                       related_name='photos',
                                       blank=True,
                                       null=True)


class Album(models.model):
    """Model for album."""

    owner = models.ForeignKey(ImagerProfile,
                              on_delete=models.CASCADE,
                              related_name='albums')

    photos = models.ManyToManyField(Photo,
                                    related_name='albums')

    title = models.CharField(max_length=255, blank=True, null=True)
    description = models.CharField(max_length=255, blank=True, null=True)
    date_published = models.DateField(blank=True, null=True)
    date_uploaded = models.DateField(auto_now=True)
    date_modified = models.DateField(auto_now=True)
    published = models.CharField(max_length=255,
                                 choice=PUBLISH_TYPE,
                                 blank=True,
                                 null=True)
    cover_photo = models.ImageField(upload_to='', blank=True, null=True)
