# Cache imports
from django.core.cache import cache

class CustomCacheMiddleware:
    """ Process View se ejecuta y chekea si hay usuario logueado
    en caso de que no esté logueado, borra el caché """

    def __init__(self, get_response):
        self.get_response = get_response

    def __call__(self, request):
        response = self.get_response(request)

        return response

    def process_view(self, request, view_func, view_args, view_kwargs):
        if not request.user.is_authenticated:
            cache.clear()