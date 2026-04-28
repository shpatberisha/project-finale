import os
from fastapi import HTTPException, Header
from dotenv import load_dotenv

load_dotenv()

API_KEY = os.getenv("API_KEY", "default-api-key-change-me")

def verify_api_key(api_key: str = Header(None)):
    """Verify API key for protected endpoints"""
    if api_key is None:
        raise HTTPException(status_code=403, detail="API key required")
    if api_key != API_KEY:
        raise HTTPException(status_code=403, detail="Invalid API key")
    return api_key
