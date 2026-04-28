import sqlite3
import os
from contextlib import contextmanager

DB_NAME = "sneakers.db"

def get_db_path():
    return DB_NAME

def init_db():
    """Initialize SQLite database with tables"""
    conn = sqlite3.connect(get_db_path())
    cursor = conn.cursor()
    
    # Create brands table
    cursor.execute("""
        CREATE TABLE IF NOT EXISTS brands (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            name TEXT NOT NULL UNIQUE
        )
    """)
    
    # Create sneakers table
    cursor.execute("""
        CREATE TABLE IF NOT EXISTS sneakers (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            name TEXT NOT NULL,
            brand_id INTEGER NOT NULL,
            product_link TEXT,
            categories TEXT,
            price REAL,
            release_year INTEGER,
            colorway TEXT,
            FOREIGN KEY (brand_id) REFERENCES brands(id) ON DELETE CASCADE
        )
    """)
    
    conn.commit()
    conn.close()

@contextmanager
def get_db():
    """Get database connection"""
    conn = sqlite3.connect(get_db_path())
    conn.row_factory = sqlite3.Row
    try:
        yield conn
    finally:
        conn.close()

# Initialize database on import
if not os.path.exists(get_db_path()):
    init_db()
