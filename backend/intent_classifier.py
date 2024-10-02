import sqlite3
import spacy

nlp = spacy.load('en_core_web_sm')

DATABASE = 'database.db'

def classify_intent(user_input):
    # Tokenize the user input
    doc = nlp(user_input.lower())
    
    # Extract individual tokens from user input
    processed_input_tokens = [token.text for token in doc]
    processed_input = ' '.join(processed_input_tokens).lower()  # Lowercase input for matching

    conn = sqlite3.connect(DATABASE)
    cursor = conn.cursor()

    # Get all keywords with their priorities from the database
    cursor.execute('SELECT intent_id, keyword, priority FROM keywords')
    keywords = cursor.fetchall()
    conn.close()

    matched_keywords = []
    
    # Group keywords by intent_id and priority
    intent_keyword_map = {}

    for intent_id, keyword, priority in keywords:
        keyword_tokens = keyword.lower().split()  # Tokenize the keyword to handle multi-word phrases

        # Check if the keyword is a whole word/phrase match in the tokenized input
        if len(keyword_tokens) == 1:
            # Handle single-word keywords
            if keyword_tokens[0] in processed_input_tokens:
                position = processed_input_tokens.index(keyword_tokens[0])
                if intent_id not in intent_keyword_map:
                    intent_keyword_map[intent_id] = []
                intent_keyword_map[intent_id].append((keyword, priority, position))
        else:
            # Handle multi-word keywords (exact phrase match)
            if ' '.join(keyword_tokens) in processed_input:
                position = processed_input.find(' '.join(keyword_tokens))
                if intent_id not in intent_keyword_map:
                    intent_keyword_map[intent_id] = []
                intent_keyword_map[intent_id].append((keyword, priority, position))

    if not intent_keyword_map:
        return {'response': "Sorry, I didn't understand tt."}

    # Find all matched keywords sorted by priority and position in the input
    sorted_keywords = sorted(
        [(intent_id, kw) for intent_id, kws in intent_keyword_map.items() for kw in kws],
        key=lambda x: (-x[1][1], x[1][2])  # Sort by priority (descending), then by position (ascending)
    )

    # Extract highest priority from the matched keywords
    highest_priority = sorted_keywords[0][1][1]
    top_priority_keywords = [(intent_id, kw[0]) for intent_id, kw in sorted_keywords if kw[1] == highest_priority]

    # Check if there are multiple keywords with the same priority
    if len(top_priority_keywords) > 1:
        # Check if all top-priority keywords have the same intent_id
        unique_intent_ids = set(intent_id for intent_id, _ in top_priority_keywords)

        if len(unique_intent_ids) == 1:
            # All keywords have the same intent_id, proceed with this intent
            return {'intent_id': list(unique_intent_ids)[0]}
        else:
            # Different intent_ids, display the options to the user
            return {
                'multiple_intents': top_priority_keywords,
                'response': "Please choose one of the following options:",
                'choices': [f"{kw} (Intent {intent_id})" for intent_id, kw in top_priority_keywords]
            }

    # If there's only one top-priority keyword or intent_id, proceed with it
    return {'intent_id': sorted_keywords[0][0]}

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
