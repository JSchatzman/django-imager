from django.test import TestCase
from django.contrib.auth.models import User
from imager_profile.models import ImagerProfile
import factory

# Create your tests here.
class ProfileTests(TestCase):
    """Run the tests."""
    class UserFactory(factory.django.DjangoModelFactory):
        """Generate test users."""
        class Meta:
            model = User
        username = factory.Sequence(lambda n: "The Chosen {}".format(n))
        email = factory.LazyAttribute(
        lambda x: "{}@imager.com".format(x.username.replace(" ", "")))

    def setUp(self):
        """set up for tests."""
        self.users = [self.UserFactory.create() for i in range(5)]

    def test_profile_made(self):
        self.assertTrue(ImagerProfile.objects.count() == 5)

    def test_profile_associated_with_users(self):
        """Test that created profiles are actually assigned to users."""
        profile = ImagerProfile.objects.first()
        self.assertTrue(hasattr(profile, 'user'))
        self.assertIsInstance(profile.user, User)

    def test_user_has_profile_attached(self):
        """Test that a user is attached to a profile."""
        user = self.users[0]
        self.assertTrue(hasattr(user, 'profile'))
        self.assertIsInstance(user.profile, ImagerProfile)

    # def test_update_profile_attribute(self):
    #     """Test that changing a attribute of a user works correctly."""
    #     user = self.users[0]
    #     user.profile.bio = 'bio'
    #     query = User.objects.first()
    #     self.assertTrue(query.profile.bio == 'bio')
