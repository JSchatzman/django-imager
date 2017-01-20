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
        username = factory.Sequence(lambda n: "User {}".format(n))
        email = factory.LazyAttribute(
        lambda x: "{}@imager.com".format(x.username.replace(" ", "")))

    def setUp(self):
        """set up for tests."""
        self.users = [self.UserFactory.create() for i in range(5)]

    def test_profile_made(self):
        """Test that a profile has been made."""
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

    def test_update_profile_attribute(self):
        """Test that changing a attribute of a user works correctly."""
        user = self.users[0]
        user.profile.bio = 'bio'
        user.profile.save()
        query = User.objects.first()
        #import pdb; pdb.set_trace()
        self.assertTrue(query.profile.bio == 'bio')

    # def test_login_route_redirects(self):
    #     """"""
    #     new_user = UserFactory.create()
    #     new_user.username = "potato_joe"
    #     new_user.set_password("tugboats")
    #     new_user.save()
    #     response = self.client.get("/login/", {
    #         "username": new_user.username,
    #         "password": "tugboats"
    #     })
    #     self.assertTrue(response.status_code == 302)

    # def test_login_route_redirects_to_homepage(self):
    #     """"""
    #     new_user = UserFactory.create()
    #     new_user.username = "potato_joe"
    #     new_user.set_password("tugboats")
    #     new_user.save()
    #     response = self.client.get("/login/", {
    #         "username": new_user.username,
    #         "password": "tugboats"
    #     }, follow=True)
    #     self.assertTrue(response.redirect_chain[0][0] == "/")

    # def test_can_register_new_user(self):
    #     """"""
    #     self.assertTrue(User.objects.count() == 0)
    #     response = self.client.post("/registration/register/", {
    #         "username": "bobdobson",
    #         "email": "bob@dob.son",
    #         "password1": "tugboats",
    #         "password2": "tugboats",
    #     })
    #     self.assertTrue(User.objects.count() == 1)

    # def test_registered_user_is_inactive(self):
    #     """"""
    #     self.client.post("/registration/register/", {
    #         "username": "bobdobson",
    #         "email": "bob@dob.son",
    #         "password1": "tugboats",
    #         "password2": "tugboats",
    #     })
    #     the_user = User.objects.first()
    #     self.assertFalse(the_user.is_active)

    # def test_successful_registration_redirects(self):
    #     """"""
    #     response = self.client.post("/registration/register/", {
    #         "username": "bobdobson",
    #         "email": "bob@dob.son",
    #         "password1": "tugboats",
    #         "password2": "tugboats",
    #     }, follow=True)
    #     self.assertTrue(response.status_code == 302)

    # def test_successful_registration_redirects_to_right_place(self):
    #     """"""
    #     response = self.client.post("/registration/register/", {
    #         "username": "bobdobson",
    #         "email": "bob@dob.son",
    #         "password1": "tugboats",
    #         "password2": "tugboats",
    #     }, follow=True)
    #     self.assertTrue(response.redirect_chain[0][0] == "/registration/registration/complete/")
