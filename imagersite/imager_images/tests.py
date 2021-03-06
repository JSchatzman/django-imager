from django.test import TestCase
from django.contrib.auth.models import User
from imager_profile.models import ImagerProfile
from imager_images.models import Photo, Album
import factory
from django.test import Client, RequestFactory
from django.urls import reverse_lazy


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

    def test_photo_no_photographer(self):
        """Test photo created without owner."""
        photo = Photo.objects.first()
        self.assertFalse(photo.photographer)

    def test_photo_photographer(self):
        """Test photo created given owner."""
        photo = Photo.objects.first()
        user1 = User.objects.first()
        photo.photographer = user1.profile
        self.assertTrue(photo.photographer)

    def test_image_has_owner(self):
        """Test that image has an owner after assignment."""
        image = Photo.objects.first()
        user1 = User.objects.first()
        image.photographer = user1.profile
        self.assertTrue(image.photographer)

    def test_owner_has_image(self):
        """Test that the owner has the image."""
        image = Photo.objects.first()
        user1 = User.objects.first()
        image.photographer = user1.profile
        image.save()
        self.assertTrue(user1.profile.photos.count() == 1)

    def test_two_images_have_owner(self):
        """Test two images have the same owner."""
        image1 = Photo.objects.all()[0]
        image2 = Photo.objects.all()[1]
        user1 = User.objects.first()
        image1.photographer = user1.profile
        image2.photographer = user1.profile
        image1.save()
        image2.save()
        self.assertTrue(image1.photographer == user1.profile)
        self.assertTrue(image2.photographer == user1.profile)


class AlbumTest(TestCase):
    """Album app test runner."""

    def setUp(self):
        """Setup for test."""
        self.users = [UserFactory.create() for i in range(10)]
        self.images = [PhotoFactory.create() for i in range(10)]
        self.album = [AlbumFactory.create() for i in range(10)]

    def test_album_title(self):
        """Test album titles."""
        self.assertTrue("Album" in Album.objects.first().title)

    def test_album_description(self):
        """Test album description."""
        album = Album.objects.first()
        album.description = "an album"
        album.save()
        self.assertTrue(Album.objects.first().description == 'an album')

    def test_album_published(self):
        """Test album published."""
        album = Album.objects.first()
        album.published = "PUBLIC"
        album.save()
        self.assertTrue(Album.objects.first().published == "PUBLIC")

    def test_album_cover_photo(self):
        """Test Album cover photo."""
        album = Album.objects.first()
        album.cover_photo = '../imagersite/static/hawks.jpg'
        album.save()
        self.assertTrue(Album.objects.first().cover_photo)

    def test_album_no_cover_photo(self):
        """Test no cover photo."""
        album = Album.objects.first()
        album.save()
        self.assertFalse(Album.objects.first().cover_photo)

    def test_album_with_no_photos(self):
        """Test that an album has no image before assignemnt."""
        album = Album.objects.first()
        self.assertTrue(album.photos.count() == 0)

    def test_image_has_no_album(self):
        """Test that the image is in an album."""
        image = Photo.objects.first()
        self.assertTrue(image.albums.count() == 0)

    def test_image_has_album(self):
        """Test that the image is in an album."""
        image = Photo.objects.first()
        album1 = Album.objects.first()
        image.albums.add(album1)
        self.assertTrue(image.albums.count() == 1)


class FrontEndTests(TestCase):
    """Front end test runner."""

    def setUp(self):
        """Test dummy."""
        self.client = Client()
        self.request = RequestFactory()

        self.users = [UserFactory.create() for i in range(5)]
        self.photos = [PhotoFactory.create() for i in range(5)]
        self.albums = [AlbumFactory.create() for i in range(5)]

    def test_all_albums_view_client_status_ok(self):
        """Functional test."""
        from imager_images.views import AllAlbumsView
        user = UserFactory.create()
        user.save()
        req = self.request.get(reverse_lazy("albums"))
        view = AllAlbumsView.as_view()
        req.user = user
        response = view(req)
        self.assertTrue(response.status_code == 200)

    def test_all_photos_view_client_status_ok(self):
        """Functional test."""
        from imager_images.views import AllPhotosView
        user = UserFactory.create()
        user.save()
        req = self.request.get(reverse_lazy("photos"))
        view = AllPhotosView.as_view()
        req.user = user
        response = view(req)
        self.assertTrue(response.status_code == 200)
