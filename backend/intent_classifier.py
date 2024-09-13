import sqlite3

DATABASE = 'database.db'

def classify_intent(user_input):
    conn = sqlite3.connect(DATABASE)
    cursor = conn.cursor()

    # Get all keywords
    cursor.execute('SELECT intent_id, keyword FROM keywords')
    keywords = cursor.fetchall()

    for intent_id, keyword in keywords:
        if keyword.lower() in user_input.lower():
            return intent_id
    
    conn.close()
    return None
