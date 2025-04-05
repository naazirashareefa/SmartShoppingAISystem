import sqlite3

def create_tables(): 
    conn = sqlite3.connect('smart_shopping.db') 
    c = conn.cursor()
    # Users table
    c.execute('''
        CREATE TABLE IF NOT EXISTS Users (
            user_id TEXT PRIMARY KEY,
            name TEXT,
            age INTEGER,
            gender TEXT,
            location TEXT,
            preferences TEXT
        );
    ''')

    # Products table
    c.execute('''
        CREATE TABLE IF NOT EXISTS Products (
            product_id TEXT PRIMARY KEY,
            name TEXT,
            category TEXT,
            price REAL,
            popularity_score REAL DEFAULT 0
        );
    ''')

    # UserActions table
    c.execute('''
        CREATE TABLE IF NOT EXISTS UserActions (
            action_id INTEGER PRIMARY KEY AUTOINCREMENT,
            user_id TEXT,
            product_id TEXT,
            action_type TEXT, -- view, cart, purchase
            timestamp DATETIME DEFAULT CURRENT_TIMESTAMP
        );
    ''')

    # Recommendations table
    c.execute('''
        CREATE TABLE IF NOT EXISTS Recommendations (
            user_id TEXT,
            product_id TEXT,
            score REAL,
            recommended_at DATETIME DEFAULT CURRENT_TIMESTAMP
        );
    ''')

    conn.commit()
    conn.close()
    print("✅ Database and tables created.")
if __name__ == '__main__':
    create_tables()