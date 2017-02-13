"""Tests for imager api."""

import factory
from django.test import TestCase
from django.contrib.auth.models import User
from imager_profile.models import ImagerProfile
from imager_images.models import Photo, Album
from imager_api.views import PhotoAPIList
from django.test import Client, RequestFactory
from rest_framework.test import APIRequestFactory


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


class ImagerAPITests(TestCase):
    """The Images App Test Runner."""

    def setUp(self):
        """User setup for tests."""
        self.client = Client()
        self.request = APIRequestFactory()
        self.users = [UserFactory.create() for i in range(10)]
        self.russell()
        self.images = [PhotoFactory.create() for i in range(10)]
        self.albums = [AlbumFactory.create() for i in range(10)]

    def russell(self, follow=False):
        """Create a dummy user named russellszn."""
        user = UserFactory.create()
        user.username = 'russellszn'
        user.set_password('testing123')
        user.save()
        return user

    def test_api_route_ok(self):
        """Test that api route works."""
        request = self.request.get('/api/v1/russellszn/')
        view = PhotoAPIList.as_view()
        response = view(request, username='russellszn')
        self.assertTrue(response.status_code == 200)

    def test_public_photos_in_response(self):
        """Assert response has photos."""
        user = User.objects.filter(username='russellszn')[0]
        photo = PhotoFactory.create()
        photo.photographer = user.profile
        photo2 = PhotoFactory.create()
        photo2.photographer = user.profile
        photo.published = 'PUBLIC'
        photo2.published = 'PUBLIC'
        photo.save()
        photo2.save()
        self.client.force_login(user)
        request = self.request.get('/api/v1/russellszn/')
        view = PhotoAPIList.as_view()
        response = view(request, username='russellszn')
        self.assertTrue(len(response.data) == 2)

    def test_private_photos_excluded_in_response(self):
        """Assert private photo excluded in response."""
        user = User.objects.filter(username='russellszn')[0]
        photo = PhotoFactory.create()
        photo.photographer = user.profile
        photo2 = PhotoFactory.create()
        photo2.photographer = user.profile
        photo.published = 'PRIVATE'
        photo2.published = 'PUBLIC'
        photo.save()
        photo2.save()
        request = self.request.get('/api/v1/russellszn/')
        view = PhotoAPIList.as_view()
        response = view(request, username='russellszn')
        self.assertTrue(len(response.data) == 1)

    def test_attributes_in_response(self):
        """Assert private photo excluded in response."""
        user = User.objects.filter(username='russellszn')[0]
        photo = PhotoFactory.create()
        photo.photographer = user.profile
        photo.published = 'PUBLIC'
        photo.description = 'test desc'
        photo.save()
        request = self.request.get('/api/v1/russellszn/')
        view = PhotoAPIList.as_view()
        response = view(request, username='russellszn')
        self.assertTrue('test desc' in str(response.data))
