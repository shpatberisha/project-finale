import sqlite3


# Function to establish a connection to the SQLite database
def get_db_connection():
    conn = sqlite3.connect('sneakers.db')
    conn.row_factory = sqlite3.Row  # This allows the rows returned to behave like dictionaries
    return conn


def create_database():
    # Set up the SQLite database
    conn = sqlite3.connect('sneakers.db')
    cursor = conn.cursor()

    # Create a table to store sneaker information
    cursor.execute('''
        CREATE TABLE IF NOT EXISTS sneakers (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            name TEXT,
            brand_id INTEGER,
            product_link TEXT,
            categories TEXT,
            price REAL,
            release_year INTEGER,
            colorway TEXT,
            FOREIGN KEY (brand_id) REFERENCES brands(id)
        )
    ''')
    cursor.execute('''
            CREATE TABLE IF NOT EXISTS brands (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                name TEXT UNIQUE
            )
        ''')
    
    # Create users table for authentication
    cursor.execute('''
        CREATE TABLE IF NOT EXISTS users (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            username TEXT UNIQUE NOT NULL,
            email TEXT UNIQUE NOT NULL,
            password_hash TEXT NOT NULL,
            is_active BOOLEAN DEFAULT 1,
            created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
        )
    ''')
    
    conn.commit()
    return conn, cursor


def insert_brands(brands, cursor):
    brand_ids = {}

    for brand in brands:
        cursor.execute('''
            INSERT OR IGNORE INTO brands (name)
            VALUES (?)
        ''', (brand,))
        cursor.execute('SELECT id FROM brands WHERE name = ?', (brand,))
        brand_ids[brand] = cursor.fetchone()[0]

    return brand_ids


def insert_sneakers(sneakers_dict, brand_ids, cursor):
    for (name, brand), info in sneakers_dict.items():
        cursor.execute('''
            INSERT INTO sneakers (name, brand_id, product_link, categories, price, release_year, colorway)
            VALUES (?, ?, ?, ?, ?, ?, ?)
        ''', (
            name,
            brand_ids[brand],
            info['link'],
            ', '.join(info['categories']),
            float(info['price'].replace('$', '').replace(',', '')) if info.get('price') else None,
            int(info['release_year']) if info.get('release_year') else None,
            info.get('colorway')
        ))


def insert_data(sneakers_dict, brands):
    conn, cursor = create_database()

    # Insert brands and get their IDs
    brand_ids = insert_brands(brands, cursor)

    # Insert sneakers using the brand IDs
    insert_sneakers(sneakers_dict, brand_ids, cursor)

    conn.commit()
    conn.close()


if __name__ == "__main__":
    from sneakers_scraper import scrape_sneakers

    # Get the scraped data
    sneakers_dict, brands = scrape_sneakers()

    # Insert the data into the database
    insert_data(sneakers_dict, brands)
