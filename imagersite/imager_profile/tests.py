from django.test import TestCase
from django.contrib.auth.models import User
from imager_profile.models import ImagerProfile
import factory

# Create your tests here.

class ImagerTests(TestCase):
    """Test case for Imager."""

    class UserFactory(factory.django.DjangoModelFactory):
        class Meta:
            model = User

        username = factory.Sequence(lambda n: "The Chosen {}".format(n))

    def setUp(self):
        """set up for tests."""
        self.users = [self.UserFactory.create() for i in range(5)]

    def test_profile_made(self):
        self.assertTrue(ImagerProfile.objects.count() == 5)