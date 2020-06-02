from django.http import HttpResponse
from django.utils.deprecation import MiddlewareMixin


class CustomCorsMiddleware:
    def __init__(self, get_response):
        self.get_response = get_response
        # One-time configuration and initialization.

    def __call__(self, request):
        # Code to be executed for each request before
        # the view (and later middleware) are called.

        response = self.get_response(request)
        response["Access-Control-Allow-Origin"] = "*"
        response["Access-Control-Allow-Headers"] = "*"
        print(response.status_code)
        print(response.content)

        # Code to be executed for each request/response after
        # the view is called.

        return response