import sqlite3
def test_cascade_delete():
    conn = sqlite3.connect('database.db')
    cursor = conn.cursor()
    cursor.execute('PRAGMA foreign_keys = ON')

    # Insert sample data
    cursor.execute('INSERT INTO intents (intent_name, has_submenu) VALUES (?, ?)', ('Test Intent', True))
    intent_id = cursor.lastrowid

    cursor.execute('INSERT INTO keywords (intent_id, keyword) VALUES (?, ?)', (intent_id, 'Test Keyword'))
    cursor.execute('INSERT INTO responses (intent_id, response) VALUES (?, ?)', (intent_id, 'Test Response'))
    cursor.execute('INSERT INTO submenu_responses (intent_id, submenu_option, submenu_response) VALUES (?, ?, ?)', (intent_id, 'Test Option', 'Test Submenu Response'))

    conn.commit()

    # Verify data inserted
    cursor.execute('SELECT * FROM intents WHERE id = ?', (intent_id,))
    print("Intent Table:", cursor.fetchall())
    cursor.execute('SELECT * FROM keywords WHERE intent_id = ?', (intent_id,))
    print("Keywords Table:", cursor.fetchall())
    cursor.execute('SELECT * FROM responses WHERE intent_id = ?', (intent_id,))
    print("Responses Table:", cursor.fetchall())
    cursor.execute('SELECT * FROM submenu_responses WHERE intent_id = ?', (intent_id,))
    print("Submenu Responses Table:", cursor.fetchall())

   
    conn.commit()

    # Verify if related records are deleted
    cursor.execute('SELECT * FROM keywords WHERE intent_id = ?', (intent_id,))
    print("Keywords Table After Deletion:", cursor.fetchall())
    cursor.execute('SELECT * FROM responses WHERE intent_id = ?', (intent_id,))
    print("Responses Table After Deletion:", cursor.fetchall())
    cursor.execute('SELECT * FROM submenu_responses WHERE intent_id = ?', (intent_id,))
    print("Submenu Responses Table After Deletion:", cursor.fetchall())

    conn.close()

test_cascade_delete()
