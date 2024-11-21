import sqlite3
import spacy
from datetime import datetime
nlp = spacy.load('en_core_web_lg')

DATABASE = 'database.db'

# Updated classify_intent with fine-tuned threshold
def classify_intent(user_input):
    # Tokenize and process the user input using spaCy
    doc = nlp(user_input.lower())
    processed_input = doc
    
    conn = sqlite3.connect(DATABASE)
    cursor = conn.cursor()

    # Get all keywords with their priorities from the database
    cursor.execute('SELECT intent_id, keyword, priority FROM keywords')
    keywords = cursor.fetchall()
    conn.close()

    matched_keywords = []
    intent_keyword_map = {}

    for intent_id, keyword, priority in keywords:
        keyword_doc = nlp(keyword.lower())  # Process the keyword using spaCy
        similarity = processed_input.similarity(keyword_doc)
        
        # Experiment with dynamic thresholds
        threshold = 0.75  # Default threshold for most intents
        if "specific query" in user_input.lower():  # Adjust threshold for specific queries
            threshold = 0.85
        elif "broad query" in user_input.lower():  # Adjust threshold for broad queries
            threshold = 0.7
        
        if similarity >= threshold:
            if intent_id not in intent_keyword_map:
                intent_keyword_map[intent_id] = []
            intent_keyword_map[intent_id].append((keyword, priority, similarity))

    if not intent_keyword_map:
        return {'response': "Sorry, I didn't understand that."}

    # Sort keywords based on similarity (descending) and priority (descending)
    sorted_keywords = sorted(
        [(intent_id, kw) for intent_id, kws in intent_keyword_map.items() for kw in kws],
        key=lambda x: (-x[1][1], x[1][2])  # Sort by priority (descending), then by similarity (descending)
    )

    # Extract highest priority keywords
    highest_priority = sorted_keywords[0][1][1]
    top_priority_keywords = [(intent_id, kw[0]) for intent_id, kw in sorted_keywords if kw[1] == highest_priority]

    # Check if there are multiple intents with the same priority
    if len(top_priority_keywords) > 1:
        # Refine by selecting the intent with the highest similarity score or context
        top_priority_keywords_sorted = sorted(top_priority_keywords, key=lambda x: -x[1])  # Sort by similarity score
        top_intent_id = top_priority_keywords_sorted[0][0]
        
        return {'intent_id': top_intent_id}

    return {'intent_id': sorted_keywords[0][0]}




def update_similar_questions(main_question, similar_questions):
    print(f"Updating similar questions for: {main_question}")
    print(f"Similar questions to insert: {similar_questions}")

    conn = sqlite3.connect(DATABASE)
    cursor = conn.cursor()

    try:
        # Clear existing entries
        cursor.execute('DELETE FROM similar_questions')

        # Insert new data
        for similar_question, similarity_score in similar_questions:
            print(f"Inserting: {main_question}, {similar_question}, {similarity_score}")
            cursor.execute(
                '''
                INSERT INTO similar_questions (main_question, similar_question, similarity_score)
                VALUES (?, ?, ?)
                ''',
                (main_question, similar_question, similarity_score)
            )

        conn.commit()
    except sqlite3.Error as e:
        print(f"Database error: {e}")
    finally:
        conn.close()




def classify_submenu_option(user_input):
    """Classify submenu option and store similar questions."""
    conn = sqlite3.connect(DATABASE)
    cursor = conn.cursor()

    # Get all submenu options
    cursor.execute('SELECT submenu_option FROM submenu_responses')
    submenu_options = cursor.fetchall()
    conn.close()

    input_doc = nlp(user_input.lower())
    threshold = 0.8  # Set a threshold for submenu matching

    best_match = None
    best_similarity = 0
    similar_questions = []

    # Compare user input with submenu options
    for submenu_option in submenu_options:
        submenu_option_doc = nlp(submenu_option[0].lower())
        similarity = input_doc.similarity(submenu_option_doc)

        # Track similar questions
        if similarity >= threshold:
            similar_questions.append((submenu_option[0], similarity))

        # Identify the best match
        if similarity > best_similarity and similarity >= threshold:
            best_similarity = similarity
            best_match = submenu_option[0]

    # Update the similar_questions table
    print(f"Similar questions to be updated: {similar_questions}")
    update_similar_questions(user_input, similar_questions)

    if not best_match:
        return {'response': "I couldn't find a specific option, could you clarify what you're looking for?"}

    return best_match