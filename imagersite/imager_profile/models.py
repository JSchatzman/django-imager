from django.db import models
from django.contrib.auth.models import User
import uuid

from django.db.models.signals import post_save # <-- after saving a thing, do a thing
from django.dispatch import receiver # <-- listen for a thing to be done

# Create your models here.


class ImagerProfile(models.Model):
    """The ImagerProfile and all of its attributes."""

    user = models.OneToOneField(
        User,
        related_name="profile",
        on_delete=models.CASCADE
    )
    hireable = models.BooleanField(default=True)
    address = models.CharField(max_length=255, blank=True, null=True)
    camera_type = models.CharField(max_length=255, blank=True, null=True)
    personal_website = models.URLField(max_length=200)
    bio = models.TextField()
    travel_radius = models.DecimalField(max_digits=8, decimal_places=2, null=True)
    phone = models.CharField(max_length=50, blank=True, null=True)
    photo_type = models.CharField(max_length=50, blank=True, null=True)
    is_active = models.BooleanField(default=True)


@receiver(post_save, sender=User)
def make_profile_for_user(sender, instance, **kwargs):
    new_profile = ImagerProfile(user=instance)
    new_profile.is_active = True
    print('Welcome to Joey, Ben, and Jordans makeprofile shell! Enjoy the complimentary drinks.')
    print('hireable', new_profile.hireable)
    print('address', new_profile.hireable)
    print('camera_type', new_profile.hireable)
    print('personal_website', new_profile.hireable)
    print('bio', new_profile.hireable)
    print('travel_radius', new_profile.hireable)
    print('phone', new_profile.hireable)
    print('photo_type', new_profile.hireable)
    print('is_active', new_profile.hireable)
    new_profile.save()
