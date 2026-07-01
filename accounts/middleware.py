from django.shortcuts import redirect
from django.conf import settings
import re

class LoginRequiredMiddleware:
    """
    Middleware that requires a user to be authenticated to view any page other
    than the explicitly exempted URLs (Splash, Login, Register, Admin, etc.)
    """
    def __init__(self, get_response):
        self.get_response = get_response
        self.exempt_urls = [
            re.compile(r'^/$'),
            re.compile(r'^/login/$'),
            re.compile(r'^/register/$'),
            re.compile(r'^/forgot-password/$'),
            re.compile(r'^/admin/'),
            re.compile(r'^/static/'),
            re.compile(r'^/media/'),
        ]

    def __call__(self, request):
        path = request.path_info

        if not request.user.is_authenticated:
            # If the user is not authenticated and the path is not exempt, redirect to login
            if not any(url.match(path) for url in self.exempt_urls):
                return redirect(settings.LOGIN_URL)

        response = self.get_response(request)
        return response
