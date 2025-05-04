import sqlite3
import os
import traceback

# Database file path
DB_FILE = 'simplified_ecommerce.db'

def create_simplified_database():
    """Create a new simplified SQLite database with schema focused on products and tags"""
    try:
        # Remove existing database if it exists
        if os.path.exists(DB_FILE):
            os.remove(DB_FILE)
        
        # Connect to the database (creates it if it doesn't exist)
        conn = sqlite3.connect(DB_FILE)
        cursor = conn.cursor()
        
        # Enable foreign keys constraint
        cursor.execute('PRAGMA foreign_keys = ON')
        
        # Create tables
        create_tables(cursor)
        
        # Commit changes and close connection
        conn.commit()
        conn.close()
        
        print(f"Database '{DB_FILE}' created successfully with simplified schema.")
    except Exception as e:
        print(f"Error creating database: {str(e)}")
        print(traceback.format_exc())

def create_tables(cursor):
    """Create the simplified tables for tag-focused product search"""
    
    # Categories table - keeping minimal but useful for organization
    cursor.execute('''
    CREATE TABLE categories (
        id INTEGER PRIMARY KEY AUTOINCREMENT,
        name TEXT NOT NULL,
        description TEXT
    )
    ''')
    
    # Products table - simplified
    cursor.execute('''
    CREATE TABLE products (
        id INTEGER PRIMARY KEY AUTOINCREMENT,
        name TEXT NOT NULL,
        sku TEXT UNIQUE,
        description TEXT,
        short_description TEXT,
        price REAL NOT NULL,
        sale_price REAL,
        category_id INTEGER,
        brand TEXT,
        is_active BOOLEAN DEFAULT 1,
        created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
        FOREIGN KEY (category_id) REFERENCES categories(id)
    )
    ''')
    
    # Tags table - this will be our main focus
    cursor.execute('''
    CREATE TABLE tags (
        id INTEGER PRIMARY KEY AUTOINCREMENT,
        name TEXT NOT NULL UNIQUE,
        description TEXT,
        created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
    )
    ''')
    
    # Product tags relationship table
    cursor.execute('''
    CREATE TABLE product_tags (
        product_id INTEGER NOT NULL,
        tag_id INTEGER NOT NULL,
        PRIMARY KEY (product_id, tag_id),
        FOREIGN KEY (product_id) REFERENCES products(id) ON DELETE CASCADE,
        FOREIGN KEY (tag_id) REFERENCES tags(id) ON DELETE CASCADE
    )
    ''')
    
    # Product images table - keeping minimal but useful for UI
    cursor.execute('''
    CREATE TABLE product_images (
        id INTEGER PRIMARY KEY AUTOINCREMENT,
        product_id INTEGER NOT NULL,
        image_url TEXT NOT NULL,
        is_primary BOOLEAN DEFAULT 0,
        FOREIGN KEY (product_id) REFERENCES products(id) ON DELETE CASCADE
    )
    ''')
    
    # Search logs - for analytics
    cursor.execute('''
    CREATE TABLE search_logs (
        id INTEGER PRIMARY KEY AUTOINCREMENT,
        search_query TEXT NOT NULL,
        results_count INTEGER,
        search_date TIMESTAMP DEFAULT CURRENT_TIMESTAMP
    )
    ''')
    
    print("Simplified database schema created successfully.")

if __name__ == "__main__":
    create_simplified_database()