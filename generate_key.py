import secrets
import os

def generate_api_key():
    """Generate a random API key"""
    api_key = secrets.token_urlsafe(32)
    
    # Create or update .env file
    with open(".env", "w") as f:
        f.write(f"API_KEY={api_key}\n")
    
    print(f"✓ API key generated and saved to .env")
    print(f"API Key: {api_key}")
    print(f"\nUse this key in the 'api-key' header for protected endpoints (POST, PUT, DELETE)")
    return api_key

if __name__ == "__main__":
    generate_api_key()
