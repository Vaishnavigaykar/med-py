import sqlite3

def create_connection():
    """Create a database connection to the SQLite database."""
    conn = sqlite3.connect('users.db')
    return conn

def setup_database():
    """Create the user table if it doesn't exist."""
    conn = create_connection()
    cursor = conn.cursor()
    cursor.execute('''
        CREATE TABLE IF NOT EXISTS users (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            username TEXT NOT NULL UNIQUE,
            password TEXT NOT NULL
        )
    ''')
    conn.commit()
    conn.close()

if __name__ == '__main__':
    setup_database()
