# intent.py
import sqlite3

DATABASE = 'database.db'

def load_intents_from_db():
    conn = sqlite3.connect(DATABASE)
    cursor = conn.cursor()

    # Get all intents
    cursor.execute('SELECT * FROM intents')
    rows = cursor.fetchall()

    intents = []
    for row in rows:
        # For each intent, load the keywords and submenu options
        intent = {
            'id': row[0],
            'intent_name': row[1],
            'has_submenu': row[2],
            'keywords': load_keywords_for_intent(row[0])
        }
        if intent['has_submenu']:
            intent['submenu_options'] = load_submenu_options_for_intent(row[0])
        intents.append(intent)

    conn.close()
    return intents

def load_keywords_for_intent(intent_id):
    conn = sqlite3.connect(DATABASE)
    cursor = conn.cursor()

    # Fetch keywords for the given intent
    cursor.execute('SELECT keyword FROM keywords WHERE intent_id = ?', (intent_id,))
    rows = cursor.fetchall()

    conn.close()
    return [row[0] for row in rows]

def load_submenu_options_for_intent(intent_id):
    conn = sqlite3.connect(DATABASE)
    cursor = conn.cursor()

    # Fetch submenu options for the given intent
    cursor.execute('SELECT submenu_option FROM submenu_responses WHERE intent_id = ?', (intent_id,))
    rows = cursor.fetchall()

    conn.close()
    return [row[0] for row in rows]
