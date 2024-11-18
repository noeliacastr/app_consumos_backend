from starlette.middleware.base import BaseHTTPMiddleware
from fastapi import Request
from fastapi import HTTPException
from services.AuthService import AuthService

"""
    Middleware que maneja la autenticación de JSON Web Tokens (JWT) en las solicitudes de FastAPI.
    Este middleware intercepta las solicitudes y verifica si el encabezado de autorización
    contiene un token válido.
    """

class JwtAuthMiddleware(BaseHTTPMiddleware):
    async def handleAuth(request: Request, call_next):
        authorizationHeader = request._headers.get("Authorization")
        if authorizationHeader is None:
            raise HTTPException(status_code=401, detail="Could not privile")
        response = AuthService.isActive(request)
        return await call_next(request)
    