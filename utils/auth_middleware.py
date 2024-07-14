from starlette.middleware.base import BaseHTTPMiddleware
from starlette.requests import Request
from starlette.responses import RedirectResponse

class AuthMiddleware(BaseHTTPMiddleware):
    async def dispatch(self, request: Request, call_next):
        if request.url.path.startswith("/static/") or request.url.path.startswith("/api") :
            return await call_next(request)
        if request.url.path.startswith("/attraction/") or request.url.path.startswith("/auth/") : 
            return await call_next(request)
        if request.url.path not in ["/", "/booking", "/thankyou", '/history_orders']:
            return RedirectResponse(url='/')
        return await call_next(request)