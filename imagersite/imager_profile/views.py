from django.shortcuts import render
from django.contrib.auth.models import User


# Create your views here.
def home_view(request, name=''):
    """View for the home page."""
    return render(request, 'imagersite/home.html', context={'name': name})


def profile_view(request, username=None):
    """View for profile page."""
    if not username:
        username = request.user.username
    user_profile = User.objects.get(username=username).profile
