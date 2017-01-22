"""Implementation of photo and album models."""


from django.db import models
from imager_profile.models import ImagerProfile


class Photo(models.model):
    """Model for photo."""

    PUBLISH_TYPE = (
        ('PRIVATE', 'Private'),
        ('SHARED', 'Shared'),
        ('PUBLIC', 'Public')
    )

    title = models.CharField(max_length=255, blank=True, null=True)
    description = models.CharField(max_length=255, blank=True, null=True)
    date_published = models.DateField(blank=True, null=True)
    date_uploaded = models.DateField(auto_now=True)
    date_modified = models.DateField(auto_now=True)
    published = models.CharField(max_length=255,
                                 choice=PUBLISH_TYPE,
                                 blank=True,
                                 null=True)
