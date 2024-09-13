import sqlite3

def update_schema():
    conn = sqlite3.connect('database.db')
    cursor = conn.cursor()

    # Check if 'submenu_options' column exists and is of the correct type
    cursor.execute("PRAGMA table_info(intents)")
    columns = cursor.fetchall()
    
    # If submenu_options is not a TEXT column, alter the table
    if not any(col[1] == 'submenu_options' and col[2] == 'TEXT' for col in columns):
        # Create a new table with the correct schema
        cursor.execute('''
        CREATE TABLE IF NOT EXISTS intents_new (
            id INTEGER PRIMARY KEY,
            name TEXT UNIQUE NOT NULL,
            keywords TEXT NOT NULL,
            has_submenu BOOLEAN NOT NULL,
            submenu_options TEXT
        )
        ''')
        
        # Copy data from old table to new table
        cursor.execute('''
        INSERT INTO intents_new (id, name, keywords, has_submenu, submenu_options)
        SELECT id, name, keywords, has_submenu, submenu_options
        FROM intents
        ''')
        
        # Drop the old table and rename the new one
        cursor.execute('DROP TABLE intents')
        cursor.execute('ALTER TABLE intents_new RENAME TO intents')
    
    conn.commit()
    conn.close()

update_schema()
