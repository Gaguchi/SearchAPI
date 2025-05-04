import sqlite3

def print_database_structure():
    """Print the structure of the ecommerce database."""
    conn = sqlite3.connect('ecommerce.db')
    cursor = conn.cursor()
    
    # Get all table names
    cursor.execute("SELECT name FROM sqlite_master WHERE type='table'")
    tables = [row[0] for row in cursor.fetchall()]
    print("Tables in database:")
    for table in tables:
        print(f"- {table}")
    
    # Print schema for each table
    print("\nDetailed schema for each table:")
    for table in tables:
        cursor.execute(f"PRAGMA table_info({table})")
        columns = cursor.fetchall()
        print(f"\nTable: {table}")
        for col in columns:
            print(f"  - {col[1]} ({col[2]})")
    
    conn.close()

if __name__ == "__main__":
    print_database_structure()