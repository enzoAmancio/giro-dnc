"""
Middleware customizado para debug de CSRF e autenticação
"""
import logging

logger = logging.getLogger(__name__)


class CSRFDebugMiddleware:
    """
    Middleware para debug de problemas CSRF
    Loga informações quando ocorre falha de CSRF
    """
    
    def __init__(self, get_response):
        self.get_response = get_response
    
    def __call__(self, request):
        # Debug de autenticação
        if request.path.startswith('/painel/'):
            print(f"🔍 Middleware Debug - {request.method} {request.path}")
            print(f"   User: {request.user}")
            print(f"   Authenticated: {request.user.is_authenticated}")
            print(f"   Session key: {request.session.session_key}")
            print(f"   Session data: {dict(request.session)}")
        
        response = self.get_response(request)
        
        # Se for erro 403 (possível CSRF)
        if response.status_code == 403:
            logger.warning(
                f"CSRF Debug - Possível erro CSRF:\n"
                f"Path: {request.path}\n"
                f"Method: {request.method}\n"
                f"User: {request.user}\n"
                f"Referer: {request.META.get('HTTP_REFERER', 'N/A')}\n"
                f"Origin: {request.META.get('HTTP_ORIGIN', 'N/A')}\n"
                f"Has CSRF Cookie: {'csrftoken' in request.COOKIES}\n"
                f"Has CSRF Token: {request.META.get('CSRF_COOKIE', 'N/A')}"
            )
        
        return response
