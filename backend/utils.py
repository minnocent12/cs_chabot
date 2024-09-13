from intents import load_intents_from_db
from responses import get_response_for_intent, get_submenu_response
from intent_classifier import classify_intent
import sqlite3

DATABASE = 'database.db'

def get_db_connection():
    """Get a connection to the SQLite database."""
    conn = sqlite3.connect(DATABASE)
    conn.row_factory = sqlite3.Row  # Allows accessing rows as dictionaries
    return conn

def close_db(conn):
    """Close the database connection."""
    if conn:
        conn.close()

def handle_input(user_input):
    # Classify the intent based on user input
    intent_id = classify_intent(user_input)
    
    if intent_id:
        # Get the response for the classified intent
        response = get_response_for_intent(intent_id)
        
        # Check if the intent has a submenu
        intent = get_intent_by_id(intent_id)
        if intent and intent['has_submenu']:
            # If the user input contains a submenu option, return the submenu response
            submenu_option = classify_submenu_option(user_input, get_submenu_options(intent_id))
            if submenu_option:
                submenu_response = get_submenu_response(intent_id, submenu_option)
                return submenu_response

        return response
    else:
        return "Sorry, I didn't understand that."

def get_intent_by_id(intent_id):
    """Retrieve intent data by ID."""
    conn = get_db_connection()
    try:
        cursor = conn.cursor()
        cursor.execute('SELECT * FROM intents WHERE id = ?', (intent_id,))
        row = cursor.fetchone()
        return dict(row) if row else None
    finally:
        close_db(conn)

def get_submenu_options(intent_id):
    """Retrieve submenu options for a given intent ID."""
    conn = get_db_connection()
    try:
        cursor = conn.cursor()
        cursor.execute('SELECT submenu_option FROM submenu_responses WHERE intent_id = ?', (intent_id,))
        rows = cursor.fetchall()
        return [row['submenu_option'] for row in rows]
    finally:
        close_db(conn)

def classify_submenu_option(user_input, submenu_options):
    """Check if the user input matches any of the submenu options."""
    for option in submenu_options:
        if option.lower() in user_input.lower():
            return option
    return None

# CRUD operations for intents
def get_intents_from_db():
    """Retrieve all intents from the database."""
    conn = get_db_connection()
    try:
        cursor = conn.cursor()
        cursor.execute('SELECT * FROM intents')
        rows = cursor.fetchall()
        return [dict(row) for row in rows]
    finally:
        close_db(conn)

def add_intent_to_db(intent_name, has_submenu):
    """Add a new intent to the database."""
    conn = get_db_connection()
    try:
        cursor = conn.cursor()
        cursor.execute('INSERT INTO intents (intent_name, has_submenu) VALUES (?, ?)', (intent_name, has_submenu))
        conn.commit()
        return cursor.rowcount > 0
    finally:
        close_db(conn)

def update_intent_in_db(intent_id, intent_name, has_submenu):
    """Update an existing intent in the database."""
    conn = get_db_connection()
    try:
        cursor = conn.cursor()
        cursor.execute('UPDATE intents SET intent_name = ?, has_submenu = ? WHERE id = ?', (intent_name, has_submenu, intent_id))
        conn.commit()
        return cursor.rowcount > 0
    finally:
        close_db(conn)

def delete_intent_from_db(intent_id):
    """Delete an intent from the database."""
    conn = get_db_connection()
    try:
        cursor = conn.cursor()
        cursor.execute('DELETE FROM intents WHERE id = ?', (intent_id,))
        conn.commit()
        return cursor.rowcount > 0
    finally:
        close_db(conn)

# CRUD operations for responses
def get_responses_from_db():
    """Retrieve all responses from the database."""
    conn = get_db_connection()
    try:
        cursor = conn.cursor()
        cursor.execute('SELECT * FROM responses')
        rows = cursor.fetchall()
        return [dict(row) for row in rows]
    finally:
        close_db(conn)

def add_response_to_db(intent_id, response):
    """Add a new response to the database."""
    conn = get_db_connection()
    try:
        cursor = conn.cursor()
        cursor.execute('INSERT INTO responses (intent_id, response) VALUES (?, ?)', (intent_id, response))
        conn.commit()
        return cursor.rowcount > 0
    finally:
        close_db(conn)

def update_response_in_db(response_id, intent_id, response):
    """Update an existing response in the database."""
    conn = get_db_connection()
    try:
        cursor = conn.cursor()
        cursor.execute('UPDATE responses SET intent_id = ?, response = ? WHERE id = ?', (intent_id, response, response_id))
        conn.commit()
        return cursor.rowcount > 0
    finally:
        close_db(conn)

def delete_response_from_db(response_id):
    """Delete a response from the database."""
    conn = get_db_connection()
    try:
        cursor = conn.cursor()
        cursor.execute('DELETE FROM responses WHERE id = ?', (response_id,))
        conn.commit()
        return cursor.rowcount > 0
    finally:
        close_db(conn)

# CRUD operations for keywords
def get_keywords_from_db():
    """Retrieve all keywords from the database."""
    conn = get_db_connection()
    try:
        cursor = conn.cursor()
        cursor.execute('SELECT * FROM keywords')
        rows = cursor.fetchall()
        return [dict(row) for row in rows]
    finally:
        close_db(conn)

def add_keyword_to_db(intent_id, keyword):
    """Add a new keyword to the database."""
    conn = get_db_connection()
    try:
        cursor = conn.cursor()
        cursor.execute('INSERT INTO keywords (intent_id, keyword) VALUES (?, ?)', (intent_id, keyword))
        conn.commit()
        return cursor.rowcount > 0
    finally:
        close_db(conn)

def update_keyword_in_db(keyword_id, intent_id, keyword):
    """Update an existing keyword in the database."""
    conn = get_db_connection()
    try:
        cursor = conn.cursor()
        cursor.execute('UPDATE keywords SET intent_id = ?, keyword = ? WHERE id = ?', (intent_id, keyword, keyword_id))
        conn.commit()
        return cursor.rowcount > 0
    finally:
        close_db(conn)

def delete_keyword_from_db(keyword_id):
    """Delete a keyword from the database."""
    conn = get_db_connection()
    try:
        cursor = conn.cursor()
        cursor.execute('DELETE FROM keywords WHERE id = ?', (keyword_id,))
        conn.commit()
        return cursor.rowcount > 0
    finally:
        close_db(conn)

# CRUD operations for submenu responses
def get_submenu_responses_from_db():
    """Retrieve all submenu responses from the database."""
    conn = get_db_connection()
    try:
        cursor = conn.cursor()
        cursor.execute('SELECT * FROM submenu_responses')
        rows = cursor.fetchall()
        return [dict(row) for row in rows]
    finally:
        close_db(conn)

def add_submenu_response_to_db(intent_id, submenu_option, submenu_response):
    """Add a new submenu response to the database."""
    conn = get_db_connection()
    try:
        cursor = conn.cursor()
        cursor.execute('INSERT INTO submenu_responses (intent_id, submenu_option, submenu_response) VALUES (?, ?, ?)', (intent_id, submenu_option, submenu_response))
        conn.commit()
        return cursor.rowcount > 0
    finally:
        close_db(conn)

def update_submenu_response_in_db(submenu_response_id, intent_id, submenu_option, submenu_response):
    """Update an existing submenu response in the database."""
    conn = get_db_connection()
    try:
        cursor = conn.cursor()
        cursor.execute('UPDATE submenu_responses SET intent_id = ?, submenu_option = ?, submenu_response = ? WHERE id = ?', (intent_id, submenu_option, submenu_response, submenu_response_id))
        conn.commit()
        return cursor.rowcount > 0
    finally:
        close_db(conn)

def delete_submenu_response_from_db(submenu_response_id):
    """Delete a submenu response from the database."""
    conn = get_db_connection()
    try:
        cursor = conn.cursor()
        cursor.execute('DELETE FROM submenu_responses WHERE id = ?', (submenu_response_id,))
        conn.commit()
        return cursor.rowcount > 0
    finally:
        close_db(conn)
