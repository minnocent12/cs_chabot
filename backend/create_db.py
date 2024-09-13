# create_db.py

import sqlite3

# Connect to SQLite database (will create it if it doesn't exist)
conn = sqlite3.connect('database.db')
cursor = conn.cursor()

# Create the intents table
cursor.execute('''
CREATE TABLE IF NOT EXISTS intents (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    intent_name TEXT NOT NULL,
    has_submenu BOOLEAN NOT NULL
)
''')

# Create the keywords table
cursor.execute('''
CREATE TABLE IF NOT EXISTS keywords (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    intent_id INTEGER NOT NULL,
    keyword TEXT NOT NULL,
    FOREIGN KEY (intent_id) REFERENCES intents(id)
)
''')

# Create the responses table
cursor.execute('''
CREATE TABLE IF NOT EXISTS responses (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    intent_id INTEGER NOT NULL,
    response TEXT NOT NULL,
    FOREIGN KEY (intent_id) REFERENCES intents(id)
)
''')

# Create the submenu_responses table
cursor.execute('''
CREATE TABLE IF NOT EXISTS submenu_responses (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    intent_id INTEGER NOT NULL,
    submenu_option TEXT NOT NULL,
    submenu_response TEXT NOT NULL,
    FOREIGN KEY (intent_id) REFERENCES intents(id)
)
''')

# Commit and close connection
conn.commit()
conn.close()

print("Database and tables created successfully.")
