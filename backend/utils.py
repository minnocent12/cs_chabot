from intents import load_intents_from_db
from responses import get_response_for_intent, get_submenu_response, get_all_submenu_options
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
    submenu_options = get_all_submenu_options()

    # Classify input for submenu options
    submenu_option = classify_submenu_option(user_input, submenu_options)

    if submenu_option:
        intent_id = get_intent_by_submenu_option(submenu_option)
        submenu_response = get_submenu_response(intent_id, submenu_option)
        return {
            'submenu_response': submenu_response,
            'submenu_options': get_submenu_options(intent_id)
        } if submenu_response else {"response": "No response found."}

    # Classify intent
    classification_result = classify_intent(user_input)

    if classification_result is None:
        return {"response": "Sorry, I didn't understand that."}

    # Handle case with multiple intents having the same priority
    if 'multiple_intents' in classification_result:
        # Display the options for the user to choose from
        intent_choices = [{"intent_id": intent_id, "keyword": keyword} for intent_id, keyword in classification_result['multiple_intents']]
        keywords = [kw['keyword'] for kw in intent_choices]

        return {
            'response': f"Please choose one of the following options:",
            'choose_keyword': keywords,  # This will show as options for the user to select from
            'intent_choices': intent_choices  # Send back the full options with their intent_ids for processing later
        }

    # If a single intent is determined
    intent_id = classification_result.get('intent_id')

    if intent_id:
        response = get_response_for_intent(intent_id)
        intent = get_intent_by_id(intent_id)

        if intent and intent['has_submenu']:
            submenu_options = get_submenu_options(intent_id)
            if response:
                return {
                    'response': response,
                    'submenu_options': submenu_options
                }
            else:
                intent_name = intent['intent_name']
                return {
                    'response': f"Choose from the following topics about {intent_name}.",
                    'submenu_options': submenu_options
                }

        return {'response': response} if response else {"response": "Sorry, I didn't understand that."}

    return {"response": "Sorry, I didn't understand that."}




def get_intent_by_submenu_option(submenu_option):
    """Retrieve intent ID based on submenu option."""
    conn = get_db_connection()
    try:
        cursor = conn.cursor()
        cursor.execute('SELECT intent_id FROM submenu_responses WHERE submenu_option = ?', (submenu_option,))
        row = cursor.fetchone()
        return row[0] if row else None
    finally:
        close_db(conn)



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
        return [row[0] for row in rows]
    finally:
        close_db(conn)

def classify_submenu_option(user_input, submenu_options):
    """Classifies a submenu option from the user input based on a list of submenu options."""
    for submenu_option in submenu_options:
        if submenu_option[0].lower() in user_input.lower():
            return submenu_option[0]  # Return the matched submenu option
    return None

def get_all_submenu_options():
    conn = get_db_connection()
    cursor = conn.cursor()
    
    cursor.execute('SELECT submenu_option FROM submenu_responses')
    submenu_options = cursor.fetchall()
    
    conn.close()
    return submenu_options



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
    """Delete an intent and its related data from the database."""
    conn = get_db_connection()
    try:
        cursor = conn.cursor()
        
        # Delete related records from other tables
        cursor.execute('DELETE FROM submenu_responses WHERE intent_id = ?', (intent_id,))
        cursor.execute('DELETE FROM responses WHERE intent_id = ?', (intent_id,))
        cursor.execute('DELETE FROM keywords WHERE intent_id = ?', (intent_id,))
        
        # Delete the intent
        cursor.execute('DELETE FROM intents WHERE id = ?', (intent_id,))
        
        conn.commit()
        
        # Check if the intent was deleted
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

def update_response_in_db(response_id, response):
    """Update an existing response in the database without updating intent_id."""
    conn = get_db_connection()
    try:
        cursor = conn.cursor()
        # Update only the response text
        cursor.execute('UPDATE responses SET response = ? WHERE id = ?', (response, response_id))
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

def add_keyword_to_db(intent_id, keyword, priority=1):
    """Add a new keyword to the database with a specified priority."""
    conn = get_db_connection()
    try:
        cursor = conn.cursor()
        cursor.execute('INSERT INTO keywords (intent_id, keyword, priority) VALUES (?, ?, ?)', (intent_id, keyword, priority))
        conn.commit()
        return cursor.rowcount > 0
    finally:
        close_db(conn)

def update_keyword_in_db(intent_id, keyword, new_priority):
    """Update the priority of an existing keyword."""
    conn = get_db_connection()
    try:
        cursor = conn.cursor()
        cursor.execute('UPDATE keywords SET priority = ? WHERE intent_id = ? AND keyword = ?', (new_priority, intent_id, keyword))
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

def update_submenu_response_in_db(submenu_response_id, submenu_option, submenu_response):
    """Update an existing submenu response in the database."""
    conn = get_db_connection()
    try:
        cursor = conn.cursor()
        cursor.execute('UPDATE submenu_responses SET submenu_option = ? , submenu_response = ? WHERE id = ?', (submenu_option, submenu_response, submenu_response_id))
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
