from fastapi import Depends, HTTPException, status
from fastapi.security import APIKeyHeader
from dotenv import load_dotenv
import os
from auth.auth_database import get_user_by_api_key

load_dotenv()
ADMIN_API_KEY = os.getenv("API_KEYS")
API_KEY_NAME = "api-key"
api_key_header = APIKeyHeader(name=API_KEY_NAME, auto_error=False)


def get_api_key(api_key: str = Depends(api_key_header)):
    """Validate API key - accepts both admin key and user-generated keys"""
    if not api_key:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="API Key is required",
        )
    
    # Check if it's the admin API key
    if api_key == ADMIN_API_KEY:
        return api_key
    
    # Check if it's a valid user API key
    user = get_user_by_api_key(api_key)
    if user.get("success"):
        return api_key
    
    raise HTTPException(
        status_code=status.HTTP_401_UNAUTHORIZED,
        detail="Invalid API Key",
    )
