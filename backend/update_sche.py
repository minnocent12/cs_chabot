import sqlite3

def clean_orphaned_records(cursor):
    cursor.execute('DELETE FROM keywords WHERE intent_id NOT IN (SELECT id FROM intents)')
    cursor.execute('DELETE FROM responses WHERE intent_id NOT IN (SELECT id FROM intents)')
    cursor.execute('DELETE FROM submenu_responses WHERE intent_id NOT IN (SELECT id FROM intents)')

def update_schema():
    # Connect to SQLite database
    conn = sqlite3.connect('database.db')
    cursor = conn.cursor()

    # Enable foreign key support
    cursor.execute('PRAGMA foreign_keys = ON')

    # Clean orphaned records
    clean_orphaned_records(cursor)

    # Create new tables with ON DELETE CASCADE
    cursor.execute('''
    CREATE TABLE IF NOT EXISTS keywords_new (
        id INTEGER PRIMARY KEY AUTOINCREMENT,
        intent_id INTEGER NOT NULL,
        keyword TEXT NOT NULL,
        FOREIGN KEY (intent_id) REFERENCES intents(id) ON DELETE CASCADE
    )
    ''')

    cursor.execute('''
    CREATE TABLE IF NOT EXISTS responses_new (
        id INTEGER PRIMARY KEY AUTOINCREMENT,
        intent_id INTEGER NOT NULL,
        response TEXT NOT NULL,
        FOREIGN KEY (intent_id) REFERENCES intents(id) ON DELETE CASCADE
    )
    ''')

    cursor.execute('''
    CREATE TABLE IF NOT EXISTS submenu_responses_new (
        id INTEGER PRIMARY KEY AUTOINCREMENT,
        intent_id INTEGER NOT NULL,
        submenu_option TEXT NOT NULL,
        submenu_response TEXT NOT NULL,
        FOREIGN KEY (intent_id) REFERENCES intents(id) ON DELETE CASCADE
    )
    ''')

    # Copy data from old tables to new tables
    cursor.execute('''
    INSERT INTO keywords_new (id, intent_id, keyword)
    SELECT id, intent_id, keyword FROM keywords
    ''')

    cursor.execute('''
    INSERT INTO responses_new (id, intent_id, response)
    SELECT id, intent_id, response FROM responses
    ''')

    cursor.execute('''
    INSERT INTO submenu_responses_new (id, intent_id, submenu_option, submenu_response)
    SELECT id, intent_id, submenu_option, submenu_response FROM submenu_responses
    ''')

    # Drop old tables
    cursor.execute('DROP TABLE IF EXISTS keywords')
    cursor.execute('DROP TABLE IF EXISTS responses')
    cursor.execute('DROP TABLE IF EXISTS submenu_responses')

    # Rename new tables to original names
    cursor.execute('ALTER TABLE keywords_new RENAME TO keywords')
    cursor.execute('ALTER TABLE responses_new RENAME TO responses')
    cursor.execute('ALTER TABLE submenu_responses_new RENAME TO submenu_responses')

    # Commit changes
    conn.commit()
    conn.close()

    print("Tables updated with ON DELETE CASCADE and data migrated successfully.")

# Run the schema update
update_schema()
