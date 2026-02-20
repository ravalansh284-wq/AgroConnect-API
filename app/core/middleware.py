from starlette.middleware.base import BaseHTTPMiddleware
from starlette.requests import Request
from jose import jwt
from app.core.security import SECRET_KEY, ALGORITHM
from app.core.context import set_current_user_id

class AuditMiddleware(BaseHTTPMiddleware):
    async def dispatch(self, request: Request, call_next):
        auth_header = request.headers.get("Authorization")
        user_id = None

        if auth_header and auth_header.startswith("Bearer "):
            token = auth_header.split(" ")[1]
            try:
                payload = jwt.decode(token, SECRET_KEY, algorithms=[ALGORITHM])
                user_id = payload.get("id") 
                set_current_user_id(user_id) 
            except Exception:
                pass
        response = await call_next(request)
        
        return response