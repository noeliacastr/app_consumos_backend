from starlette.middleware.base import BaseHTTPMiddleware, DispatchFunction
from fastapi import Request, Response
from fastapi.responses import JSONResponse
from starlette.types import ASGIApp
from services.AuthService import AuthService

"""
    Middleware para gestionar la autenticación de las solicitudes en una aplicación FastAPI.
    
    Este middleware intercepta las solicitudes entrantes y verifica si se proporciona un token de autorización en el encabezado.
    Si el token está presente, lo valida utilizando el servicio de autenticación `AuthService`. 
    Si la validación falla (código de estado 401), devuelve una respuesta de error. 
    Las solicitudes a las rutas excluidas o aquellas que utilizan el método OPTIONS no requieren autenticación.
    """


class AuthMiddleware(BaseHTTPMiddleware):
    def __init__(
        self,
        app: ASGIApp,
        dispatch: DispatchFunction | None = None,
        excludePaths: list = [],
    ) -> None:
        super().__init__(app, dispatch)
        self.excludePaths = excludePaths

    async def dispatch(self, request: Request, call_next):
        if request.url.path not in self.excludePaths and request.method != "OPTIONS":
            token = request.headers.get("authorization")
            if token is not None:
                response = AuthService.checkToken(token)
                if response.status_code == 401:
                    return response
                else:
                    response = await call_next(request)
            else:
                return JSONResponse(
                    status_code=401, content="Could not validate credentials"
                )
        else:
            response = await call_next(request)
        return response
