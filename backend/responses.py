import sqlite3

DATABASE = 'database.db'

def get_response_for_intent(intent_id):
    conn = sqlite3.connect(DATABASE)
    cursor = conn.cursor()

    # Fetch the response for the given intent
    cursor.execute('SELECT response FROM responses WHERE intent_id = ?', (intent_id,))
    row = cursor.fetchone()

    conn.close()
    if row:
        return row[0]
    return None

def get_submenu_response(intent_id, submenu_option):
    conn = sqlite3.connect(DATABASE)
    cursor = conn.cursor()

    # Fetch the submenu response for the given intent and submenu option
    cursor.execute('SELECT submenu_response FROM submenu_responses WHERE intent_id = ? AND submenu_option = ?', (intent_id, submenu_option))
    row = cursor.fetchone()

    conn.close()
    if row:
        return row[0]
    return None



def get_all_submenu_options():
    conn = sqlite3.connect(DATABASE)
    cursor = conn.cursor()

    cursor.execute('SELECT submenu_option FROM submenu_responses')
    rows = cursor.fetchall()

    conn.close()
    return [row[0] for row in rows]
