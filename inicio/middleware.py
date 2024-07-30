from django.shortcuts import redirect
from django.urls import reverse, resolve, NoReverseMatch
from django.urls.exceptions import Resolver404
import logging

logger = logging.getLogger(__name__)

class LoginRequiredMiddleware:
    def __init__(self, get_response):
        self.get_response = get_response

    def __call__(self, request):
        try:
            exempt_urls = [
                reverse('inicio'),
                reverse('loginregister'),
                reverse('base'),
                reverse('password_reset'),
                reverse('password_reset_done'),
                reverse('password_reset_complete'),
                reverse('acceso_denegado'),
                reverse('about'),
                reverse('cuidados'),
            ]
        except NoReverseMatch:
            # Manejo de excepción si alguna URL no se puede resolver
            exempt_urls = []

        password_reset_confirm_prefix = '/password_reset_confirm/'

        if not request.user.is_authenticated:
            logger.info(f"Usuario no autenticado intentando acceder a: {request.path_info}")
            if request.path_info not in exempt_urls and not request.path_info.startswith(password_reset_confirm_prefix):
                return redirect('acceso_denegado')

        response = self.get_response(request)
        return response
