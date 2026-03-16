from fastapi.security import HTTPBearer, HTTPAuthorizationCredentials
from fastapi import HTTPException, Depends
from src.config import get_env
env = get_env()
bearer = HTTPBearer()

def verify_bearer_token(credentials: HTTPAuthorizationCredentials = Depends(bearer)):
    if credentials.credentials != env.BEARER_TOKEN:
        raise HTTPException(status_code=401, detail="Invalid token")