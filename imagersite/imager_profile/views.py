from django.shortcuts import render


# Create your views here.
def home_view(request, name=''):
    """View for the home page."""
    return render(request, 'imagersite/home.jinja2', context={'name': name})
