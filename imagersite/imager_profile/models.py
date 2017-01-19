from django.db import models
from django.contrib.auth.models import User
import uuid

from django.db.models.signals import post_save
from django.dispatch import receiver

# Create your models here.


class ActiveUsersManager(models.Manager):
    """Active user manager."""
    def get_querysets(self):
        """Get the query set of active users."""
        return super(ActiveUsersManager, self).get_querysets().filter(user__is_active__=True)


class ImagerProfile(models.Model):
    """The ImagerProfile and all of its attributes."""

    user = models.OneToOneField(
        User,
        related_name="profile",
        on_delete=models.CASCADE
    )
    active = ActiveUsersManager()
    hireable = models.BooleanField(default=True)
    address = models.CharField(max_length=255, blank=True, null=True)
    camera_type = models.CharField(max_length=255, blank=True, null=True)
    personal_website = models.URLField(max_length=200)
    bio = models.TextField()
    travel_radius = models.DecimalField(max_digits=8, decimal_places=3, null=True)
    phone = models.CharField(max_length=50, blank=True, null=True)
    photo_type = models.CharField(max_length=50, blank=True, null=True)

    def display_properties(self):
        """Print the properties of this profile."""
        print(self.hireable)
        print(self.address)
        print(self.camera_type)
        print(self.personal_website)
        print(self.bio)
        print(self.travel_radius)
        print(self.phone)
        print(self.photo_type)

    @property
    def is_active(self):
        """Return True if user is active."""
        return self.user.is_active


@receiver(post_save, sender=User)
def make_profile_for_user(sender, instance, **kwargs):
    new_profile = ImagerProfile(user=instance)
    if kwargs['created']:
        profile = ImagerProfile(user=instance)
        profile.save()
