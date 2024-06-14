from starlette.middleware.base import BaseHTTPMiddleware
from starlette.requests import Request
from starlette.responses import RedirectResponse

class AuthMiddleware(BaseHTTPMiddleware):
    async def dispatch(self, request: Request, call_next):
        if request.url.path.startswith("/static/") or request.url.path.startswith("/api/attractions") or request.url.path.startswith("/api/attraction") or request.url.path.startswith("/api/mrts"):
            return await call_next(request)
        if request.url.path.startswith("/attraction/") :
            return await call_next(request)
        if request.url.path not in ["/", "/booking", "/thankyou"]:
            return RedirectResponse(url='/')
        return await call_next(request)