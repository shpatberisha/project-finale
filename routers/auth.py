from fastapi import APIRouter, HTTPException, status
from models.user import UserCreate, UserLogin, UserResponse, Token
from database import get_db_connection
import hashlib
import secrets
from datetime import datetime, timedelta

router = APIRouter()

# Simple token storage (in production, use Redis or database)
active_tokens = {}


def hash_password(password: str) -> str:
    """Hash password using SHA256"""
    return hashlib.sha256(password.encode()).hexdigest()


def verify_password(plain_password: str, hashed_password: str) -> bool:
    """Verify password against hash"""
    return hash_password(plain_password) == hashed_password


def create_token(user_id: int) -> str:
    """Create a simple authentication token"""
    token = secrets.token_urlsafe(32)
    active_tokens[token] = {
        "user_id": user_id,
        "expires": datetime.now() + timedelta(hours=24)
    }
    return token


def validate_token(token: str) -> Optional[int]:
    """Validate token and return user_id if valid"""
    if token in active_tokens:
        token_data = active_tokens[token]
        if datetime.now() < token_data["expires"]:
            return token_data["user_id"]
        else:
            del active_tokens[token]
    return None


from typing import Optional


@router.post("/register", response_model=Token)
def register(user: UserCreate):
    """Register a new user"""
    conn = get_db_connection()
    cursor = conn.cursor()
    
    # Check if username already exists
    cursor.execute("SELECT id FROM users WHERE username = ?", (user.username,))
    if cursor.fetchone():
        conn.close()
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="Username already registered"
        )
    
    # Check if email already exists
    cursor.execute("SELECT id FROM users WHERE email = ?", (user.email,))
    if cursor.fetchone():
        conn.close()
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="Email already registered"
        )
    
    # Hash password and create user
    hashed_password = hash_password(user.password)
    cursor.execute(
        "INSERT INTO users (username, email, password_hash, is_active) VALUES (?, ?, ?, ?)",
        (user.username, user.email, hashed_password, True)
    )
    conn.commit()
    
    # Get the created user
    user_id = cursor.lastrowid
    cursor.execute("SELECT id, username, email, is_active FROM users WHERE id = ?", (user_id,))
    row = cursor.fetchone()
    conn.close()
    
    # Create token
    token = create_token(user_id)
    
    return Token(
        access_token=token,
        token_type="bearer",
        user=UserResponse(
            id=row["id"],
            username=row["username"],
            email=row["email"],
            is_active=row["is_active"]
        )
    )


@router.post("/login", response_model=Token)
def login(user: UserLogin):
    """Login user and return token"""
    conn = get_db_connection()
    cursor = conn.cursor()
    
    # Find user by username
    cursor.execute(
        "SELECT id, username, email, password_hash, is_active FROM users WHERE username = ?",
        (user.username,)
    )
    row = cursor.fetchone()
    conn.close()
    
    if not row:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Invalid username or password"
        )
    
    # Verify password
    if not verify_password(user.password, row["password_hash"]):
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Invalid username or password"
        )
    
    # Check if user is active
    if not row["is_active"]:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="User account is disabled"
        )
    
    # Create token
    token = create_token(row["id"])
    
    return Token(
        access_token=token,
        token_type="bearer",
        user=UserResponse(
            id=row["id"],
            username=row["username"],
            email=row["email"],
            is_active=row["is_active"]
        )
    )


@router.post("/logout")
def logout(token: str):
    """Logout user by invalidating token"""
    if token in active_tokens:
        del active_tokens[token]
        return {"message": "Successfully logged out"}
    return {"message": "Token not found or already expired"}


@router.get("/me", response_model=UserResponse)
def get_current_user(token: str):
    """Get current user info from token"""
    user_id = validate_token(token)
    if not user_id:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Invalid or expired token"
        )
    
    conn = get_db_connection()
    cursor = conn.cursor()
    cursor.execute("SELECT id, username, email, is_active FROM users WHERE id = ?", (user_id,))
    row = cursor.fetchone()
    conn.close()
    
    if not row:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="User not found"
        )
    
    return UserResponse(
        id=row["id"],
        username=row["username"],
        email=row["email"],
        is_active=row["is_active"]
    )
