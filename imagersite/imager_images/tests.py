from django.test import TestCase
from django.contrib.auth.models import User
from imager_profile.models import ImagerProfile
from imager_images.models import Photo, Album
import factory


class UserFactory(factory.django.DjangoModelFactory):
    """Generate test users."""

    class Meta:
        model = User
    username = factory.Sequence(lambda n: "User {}".format(n))
    email = factory.LazyAttribute(
        lambda x: "{}@imager.com".format(x.username.replace(" ", "")))


class PhotoFactory(factory.django.DjangoModelFactory):
    class Meta:
        model = Photo
    title = factory.Sequence(lambda n: "Photo {}".format(n))


class AlbumFactory(factory.django.DjangoModelFactory):
    class Meta:
        model = Album
    title = factory.Sequence(lambda n: "Album {}".format(n))


class ImagesTests(TestCase):
    """The Images App Test Runner."""

    def setUp(self):
        """User setup for tests."""
        self.users = [UserFactory.create() for i in range(10)]
        self.images = [PhotoFactory.create() for i in range(10)]
        self.album = [AlbumFactory.create() for i in range(10)]

    def test_photo_title(self):
        """Test created photo models for titles."""
        self.assertTrue("Photo" in Photo.objects.first().title)

    def test_photo_description(self):
        """Test created photo models for descriptions when added."""
        photo = Photo.objects.first()
        photo.description = "Hallelujah"
        photo.save()
        self.assertTrue(Photo.objects.first().description == "Hallelujah")

    def test_photo_published(self):
        """Test created photo models for published field when added."""
        photo = Photo.objects.first()
        photo.published = "SHARED"
        photo.save()
        self.assertTrue(Photo.objects.first().published == "SHARED")

    def test_photo_no_phototographer(self):
        """Test photo created without owner."""
        photo = Photo.objects.first()
        self.assertFalse(photo.phototographer)

    def test_photo_phototographer(self):
        """Test photo created given owner."""
        photo = Photo.objects.first()
        user1 = User.objects.first()
        photo.phototographer = user1.profile
        self.assertTrue(photo.phototographer)
