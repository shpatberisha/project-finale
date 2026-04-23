import sqlite3
import hashlib
import secrets
import os


def get_auth_db_connection():
    """Get connection to the authentication database"""
    db_path = os.path.join(os.path.dirname(__file__), '..', 'users.db')
    conn = sqlite3.connect(db_path)
    conn.row_factory = sqlite3.Row
    return conn


def create_users_table():
    """Create the users table if it doesn't exist"""
    conn = get_auth_db_connection()
    cursor = conn.cursor()
    cursor.execute('''
        CREATE TABLE IF NOT EXISTS users (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            username TEXT UNIQUE NOT NULL,
            email TEXT UNIQUE NOT NULL,
            password_hash TEXT NOT NULL,
            api_key TEXT UNIQUE,
            created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
        )
    ''')
    conn.commit()
    conn.close()


def hash_password(password: str) -> str:
    """Hash a password using SHA-256 with salt"""
    salt = "sneakers_app_salt_2024"
    return hashlib.sha256(f"{password}{salt}".encode()).hexdigest()


def generate_api_key() -> str:
    """Generate a unique API key"""
    return secrets.token_hex(32)


def create_user(username: str, email: str, password: str) -> dict:
    """Create a new user and return user data with API key"""
    create_users_table()
    conn = get_auth_db_connection()
    cursor = conn.cursor()
    
    try:
        password_hash = hash_password(password)
        api_key = generate_api_key()
        
        cursor.execute(
            "INSERT INTO users (username, email, password_hash, api_key) VALUES (?, ?, ?, ?)",
            (username, email, password_hash, api_key)
        )
        conn.commit()
        user_id = cursor.lastrowid
        
        return {
            "id": user_id,
            "username": username,
            "email": email,
            "api_key": api_key,
            "success": True
        }
    except sqlite3.IntegrityError as e:
        if "username" in str(e):
            return {"success": False, "error": "Username already exists"}
        elif "email" in str(e):
            return {"success": False, "error": "Email already exists"}
        return {"success": False, "error": "User already exists"}
    finally:
        conn.close()


def authenticate_user(username: str, password: str) -> dict:
    """Authenticate a user and return user data"""
    create_users_table()
    conn = get_auth_db_connection()
    cursor = conn.cursor()
    
    password_hash = hash_password(password)
    cursor.execute(
        "SELECT id, username, email, api_key FROM users WHERE username = ? AND password_hash = ?",
        (username, password_hash)
    )
    user = cursor.fetchone()
    conn.close()
    
    if user:
        return {
            "id": user[0],
            "username": user[1],
            "email": user[2],
            "api_key": user[3],
            "success": True
        }
    return {"success": False, "error": "Invalid username or password"}


def get_user_by_api_key(api_key: str) -> dict:
    """Get user data by API key"""
    create_users_table()
    conn = get_auth_db_connection()
    cursor = conn.cursor()
    
    cursor.execute(
        "SELECT id, username, email, api_key FROM users WHERE api_key = ?",
        (api_key,)
    )
    user = cursor.fetchone()
    conn.close()
    
    if user:
        return {
            "id": user[0],
            "username": user[1],
            "email": user[2],
            "api_key": user[3],
            "success": True
        }
    return {"success": False, "error": "Invalid API key"}


def regenerate_api_key(user_id: int) -> dict:
    """Regenerate API key for a user"""
    conn = get_auth_db_connection()
    cursor = conn.cursor()
    
    new_api_key = generate_api_key()
    cursor.execute(
        "UPDATE users SET api_key = ? WHERE id = ?",
        (new_api_key, user_id)
    )
    conn.commit()
    
    if cursor.rowcount > 0:
        conn.close()
        return {"success": True, "api_key": new_api_key}
    
    conn.close()
    return {"success": False, "error": "User not found"}
