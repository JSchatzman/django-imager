from django.test import TestCase, Client, RequestFactory
from django.contrib.auth.models import User
from imager_profile.models import ImagerProfile
from imager_profile.views import ProfileView, HomeView
import factory


class UserFactory(factory.django.DjangoModelFactory):
    """Generate test users."""

    class Meta:
        model = User
    username = factory.Sequence(lambda n: "User {}".format(n))
    email = factory.LazyAttribute(
        lambda x: "{}@imager.com".format(x.username.replace(" ", "")))



class ProfileTests(TestCase):

    """Run the tests."""

    def setUp(self):
        """set up for tests."""
        self.users = [UserFactory.create() for i in range(5)]

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
        self.assertTrue(query.profile.bio == 'bio')


class ProfileFrontEndTests(TestCase):

    def setUp(self):
        self.client = Client()
        self.request = RequestFactory()

    def test_home_view_is_status_ok(self):
        """Test route to home view without client info or headers."""
        from imager_profile.views import HomeView
        req = self.request.get("/")
        view = HomeView.as_view()
        response = view(req)
        self.assertTrue(response.status_code == 200)

    def test_home_route_is_status_ok(self):
        """Test route using client's headers, etc."""
        response = self.client.get("/")
        self.assertTrue(response.status_code == 200)

    def test_login_route_is_status_ok(self):
        """Test route using client's headers, etc."""
        response = self.client.get("/login/")
        self.assertTrue(response.status_code == 200)

    def test_invalid_route_is_status_404(self):
        """Test that invalid route returns error."""
        response = self.client.get("/bad")
        self.assertTrue(response.status_code == 404)

    def test_home_route_context_foo(self):
        """Test that home route has the right context info."""
        response = self.client.get("/")
        self.assertContains(response, 'Imager Site')

    def test_home_route_uses_right_templates(self):
        """Check that home page is using the right templates."""
        response = self.client.get("/")
        self.assertTemplateUsed(response, "layout.html")

    def test_login_route_redirects(self):
        """Test that login redirects users."""
        new_user = UserFactory.create()
        new_user.save()
        new_user.username = "testname123"
        new_user.set_password("testpassword123")
        new_user.save()
        response = self.client.post("/login/", {
            "username": new_user.username,
            "password": "testpassword123",
            })
        self.assertTrue(response.status_code == 302)

    def test_login_route_redirects_to_homepage(self):
        """Test that login redirects users to homepage."""
        new_user = UserFactory.create()
        new_user.save()
        new_user.username = "username123"
        new_user.set_password("testing123")
        new_user.save()
        response = self.client.post("/login/", {
            "username": new_user.username,
            "password": "testing123",
            }, follow=True)
        self.assertTrue(response.redirect_chain[0][0] == "/")

    def register_bob(self, follow=False):
        """Create a dummy user named russellszn."""
        response = self.client.post("/registration/register/", {
            "username": "russellszn",
            "email": "go@hawks.com",
            "password1": "testing123",
            "password2": "testing123",
        }, follow=follow)
        return response


    def add_testuser(self):
        """Make testuser and return his profile."""
        user = UserFactory.create()
        user.username = 'testuser'
        user.set_password('testuser')
        user.save()
        return user.profile

    def test_can_register_new_user(self):
        """Post request properly filled out creates new user."""
        self.assertTrue(User.objects.count() == 0)
        self.register_bob()
        self.assertTrue(User.objects.count() == 1)

    def test_registered_user_is_inactive(self):
        """Test that a newly registered user is not yet activated."""
        self.register_bob()
        the_user = User.objects.first()
        self.assertFalse(the_user.is_active)

    def test_successful_registration_redirects(self):
        """Test that registration redirects."""
        response = self.register_bob()
        self.assertTrue(response.status_code == 302)

    def test_successful_registration_redirects_to_right_place(self):
        """Test that registration redirects to registration complete page."""
        response = self.register_bob(follow=True)
        self.assertTrue(
            response.redirect_chain[0][0] == '/registration/register/complete/')

    def test_profile_page_returns_correct_html(self):
        """Test that accessing test profile returns correct html."""
        self.add_testuser()
        response = self.client.get('/profile/testuser/')
        #import pdb; pdb.set_trace()
        self.assertContains(response, 'Album Count')

    def test_profile_route_uses_right_templates(self):
        """Check that profile page is using the right templates."""
        self.add_testuser()
        response = self.client.get("/profile/testuser/")
        self.assertTemplateUsed(response, "layout.html")


class EditProfileTest(TestCase):
    """Test edit profile."""

    def setUp(self):
        self.client = Client()
        self.request = RequestFactory()

    def test_view_status(self):
        """Test 200 code."""
        from imager_profile.views import EditProfileView
        self.add_testuser()
        req = self.client.get("/profile/testuser/edit")
        view = EditProfileView.as_view()
        response = view(req)
        self.assertTrue(response.status_code == 200)