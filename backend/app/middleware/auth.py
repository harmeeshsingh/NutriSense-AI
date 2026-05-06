from fastapi import Request, status
from fastapi.responses import JSONResponse
from starlette.middleware.base import BaseHTTPMiddleware
from google.oauth2 import id_token
from google.auth.transport import requests as google_requests
from app.config import get_settings
import structlog

logger = structlog.get_logger()

class GCIPAuthMiddleware(BaseHTTPMiddleware):
    async def dispatch(self, request: Request, call_next):
        if request.url.path in ["/health", "/ready", "/docs", "/openapi.json"]:
            return await call_next(request)
            
        auth_header = request.headers.get("Authorization")
        if not auth_header or not auth_header.startswith("Bearer "):
            return JSONResponse(
                status_code=status.HTTP_401_UNAUTHORIZED,
                content={"detail": "Missing or invalid authorization header"}
            )
            
        token = auth_header.split(" ")[1]
        settings = get_settings()
        
        try:
            # Verify the token against Google's servers
            user_info = id_token.verify_oauth2_token(
                token, 
                google_requests.Request(), 
                settings.GOOGLE_CLIENT_ID
            )
            request.state.user = user_info
        except ValueError as e:
            logger.warning(f"Invalid token: {e}")
            return JSONResponse(
                status_code=status.HTTP_401_UNAUTHORIZED,
                content={"detail": "Invalid token"}
            )
            
        return await call_next(request)
