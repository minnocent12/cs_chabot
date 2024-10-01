import sqlite3
import spacy

nlp = spacy.load('en_core_web_sm')

DATABASE = 'database.db'

def classify_intent(user_input):
    doc = nlp(user_input.lower())  # Process the user input with spaCy

    conn = sqlite3.connect(DATABASE)
    cursor = conn.cursor()

    # Get all keywords with their priorities
    cursor.execute('SELECT intent_id, keyword, priority FROM keywords')
    keywords = cursor.fetchall()
    conn.close()

    matched_keywords = []
    processed_input = ' '.join([token.text for token in doc]).lower()

    for intent_id, keyword, priority in keywords:
        if keyword.lower() in processed_input:  # Match keywords case-insensitively
            position = processed_input.find(keyword.lower())  # Find keyword position in input
            matched_keywords.append((intent_id, keyword, priority, position))

    if not matched_keywords:
        return None

    # Sort matched keywords by priority (higher first) and by position (lower first)
    matched_keywords.sort(key=lambda x: (-x[2], x[3]))

    return matched_keywords[0][0]  # Return the intent_id with highest priority and first occurrence



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
