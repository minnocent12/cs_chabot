import sqlite3

DATABASE = 'database.db'

def classify_intent(user_input):
    conn = sqlite3.connect(DATABASE)
    cursor = conn.cursor()

    # Get all keywords for intents
    cursor.execute('SELECT intent_id, keyword FROM keywords')
    keywords = cursor.fetchall()

    conn.close()

    # Check if any keyword matches the user input
    for intent_id, keyword in keywords:
        if keyword.lower() in user_input.lower():
            return intent_id
    
    return None

def classify_submenu_option(user_input):
    conn = sqlite3.connect(DATABASE)
    cursor = conn.cursor()

    # Get all submenu options
    cursor.execute('SELECT submenu_option FROM submenu_responses')
    submenu_options = cursor.fetchall()

    conn.close()

    # Check if any submenu option matches the user input
    for submenu_option in submenu_options:
        if submenu_option[0].lower() in user_input.lower():
            return submenu_option[0]  # Return the matched submenu option

    return None
