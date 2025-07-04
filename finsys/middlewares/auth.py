from django.conf import settings
from django.shortcuts import redirect
from django.urls import resolve


class LoginRequiredMiddleware:
    def __init__(self, get_response):
        self.get_response = get_response

    def __call__(self, request):
        resolver_match = resolve(request.path_info)
        app_name = resolver_match.app_name or resolver_match.func.__module__.split('.')[0]

        target_app = 'finsys'

        if app_name == target_app and not request.user.is_authenticated:
            return redirect(settings.LOGIN_URL)

        return self.get_response(request)
