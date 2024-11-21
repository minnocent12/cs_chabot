import spacy
import sqlite3
from intents import load_intents_from_db
from responses import get_response_for_intent, get_submenu_response, get_all_submenu_options
from intent_classifier import classify_intent
from typing import List, Tuple
import fitz  # PyMuPDF

nlp = spacy.load('en_core_web_lg')  # Load the larger spaCy model for better accuracy

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
        

def update_similar_questions(main_question: any, similar_questions):
    """
    Update the `similar_questions` table with new data.
    Deletes existing data before inserting new entries.
    """
    conn = sqlite3.connect(DATABASE)
    cursor = conn.cursor()

    print("Clearing similar_questions table...")
    cursor.execute('DELETE FROM similar_questions')

    print("Inserting new similar questions...")
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
    conn.close()




def classify_submenu_option(user_input: str, submenu_options: List[Tuple[str]]) -> str:
    """Classifies a submenu option based on similarity to a list of submenu options."""
    doc1 = nlp(user_input.lower())
    similarity_threshold = 0.9  # Threshold for matching
    
    best_match = None
    best_similarity = 0
    similar_questions = []
    
    for submenu_option in submenu_options:
        doc2 = nlp(submenu_option[0].lower())
        similarity = doc1.similarity(doc2)
        
        # Track similar questions
        if similarity >= similarity_threshold:
            similar_questions.append((submenu_option[0], similarity))
        
        if similarity > best_similarity and similarity >= similarity_threshold:
            best_similarity = similarity
            best_match = submenu_option[0]  # Store the best matching option
            
    update_similar_questions(user_input, similar_questions)
     
    return best_match  # Return the best match if found, otherwise None

def classify_intent(user_input: str) -> dict:
    """Classifies intent based on keywords and similarity using NLP."""
    doc = nlp(user_input.lower())
    processed_input_tokens = [token.text for token in doc if not token.is_stop and not token.is_punct]
    processed_input = ' '.join(processed_input_tokens).lower()
    
    conn = get_db_connection()
    cursor = conn.cursor()
    cursor.execute('SELECT intent_id, keyword, priority FROM keywords')
    keywords = cursor.fetchall()
    conn.close()

    intent_keyword_map = {}
    nlp_similarity_threshold = 0.7  # Lower threshold for partial matches

    for intent_id, keyword, priority in keywords:
        keyword_doc = nlp(keyword.lower())
        
        # Direct similarity (sentence-to-keyword)
        similarity = doc.similarity(keyword_doc)
        
        # Partial match: Check token similarity for better coverage
        token_similarities = [token.similarity(keyword_doc) for token in doc if not token.is_stop and not token.is_punct]
        partial_similarity = max(token_similarities) if token_similarities else 0

        # Use max of direct or partial match for final score
        final_similarity = max(similarity, partial_similarity)

        if final_similarity >= nlp_similarity_threshold:
            if intent_id not in intent_keyword_map:
                intent_keyword_map[intent_id] = []
            intent_keyword_map[intent_id].append((keyword, priority, final_similarity))

    if not intent_keyword_map:
        return {'response': "Sorry, I didn't understand that."}

    # Sort by priority and similarity
    sorted_keywords = sorted(
        [(intent_id, kw) for intent_id, kws in intent_keyword_map.items() for kw in kws],
        key=lambda x: (-x[1][1], x[1][2])  # Priority descending, then similarity descending
    )

    # Extract highest priority matches
    highest_priority = sorted_keywords[0][1][1]
    top_priority_keywords = [(intent_id, kw[0]) for intent_id, kw in sorted_keywords if kw[1] == highest_priority]

    # Handle multiple intents with similar priority
    if len(top_priority_keywords) > 1:
        unique_intent_ids = set(intent_id for intent_id, _ in top_priority_keywords)
        if len(unique_intent_ids) == 1:
            return {'intent_id': list(unique_intent_ids)[0]}
        else:
            return {
                'multiple_intents': top_priority_keywords,
                'response': "Please choose one of the following options:",
                'choices': [f"{kw} (Intent {intent_id})" for intent_id, kw in top_priority_keywords]
            }

    return {'intent_id': sorted_keywords[0][0]}




def handle_input(user_input: str, pdf_id: int = None) -> dict:
    # Step 1: Check if the user is querying a PDF document (if a PDF ID is provided)
    if pdf_id:
        pdf_content = get_pdf_content(pdf_id)
        if pdf_content:
            answer = search_document_for_answer(user_input, pdf_content)
            if answer:  # Ensure we have an answer before returning it
                return {"response": answer}
            return {"response": "I'm sorry, I couldn't find an exact answer to your question in the PDF."}
        return {"response": "The requested document is not available."}

    # Step 2: Handle submenu options
    submenu_options = get_all_submenu_options()
    submenu_option = classify_submenu_option(user_input, submenu_options)

    if submenu_option:
        intent_id = get_intent_by_submenu_option(submenu_option)
        submenu_response = get_submenu_response(intent_id, submenu_option)
        intent = get_intent_by_id(intent_id)
        if submenu_response and intent:
            return {
                'submenu_response': submenu_response,
                'response': submenu_response
            }
        else:
            return {"response": "Sorry, I couldn't get a response for that option."}

    # Step 3: Classify the user's intent
    classification_result = classify_intent(user_input)

    if classification_result is None:
        return {"response": "Sorry, I didn't understand that."}

    # Step 4: Handle multiple intent options
    if 'multiple_intents' in classification_result:
        intent_choices = [{"intent_id": intent_id, "keyword": keyword} for intent_id, keyword in classification_result['multiple_intents']]
        keywords = [kw['keyword'] for kw in intent_choices]
        return {
            'response': "Please choose one of the following topics:",
            'choose_keyword': keywords,
            'intent_choices': intent_choices
        }

    # Step 5: Process intent response and submenu options if applicable
    intent_id = classification_result.get('intent_id')
    if intent_id:
        response = get_response_for_intent(intent_id)
        intent = get_intent_by_id(intent_id)
        if intent and intent['has_submenu']:
            submenu_options = get_submenu_options(intent_id)
            submenu_message = f"Choose from the following questions about {intent['intent_name']}:"
            return {
                'response': submenu_message,
                'submenu_options': submenu_options
            }
        return {'response': response} if response else {"response": "I'm having trouble understanding that."}

    # Default response if nothing matches
    return {"response": "Sorry, I didn't understand that. Try entering a short phrase, such as 'How do I request to transfer a graduate course?' or 'What should I do if a class is full?'"}

def search_document_for_answer(question: str, pdf_content: str) -> str:
    question_doc = nlp(question.lower())
    doc_sections = pdf_content.split('\n\n')  # Split by paragraphs or sections
    best_match = ""
    best_similarity = 0

    for section in doc_sections:
        section_doc = nlp(section.lower())
        similarity = question_doc.similarity(section_doc)
        if similarity > best_similarity:
            best_similarity = similarity
            best_match = section

    # Define a threshold for returning a match
    if best_similarity >= 0.5:  # Lower the threshold to allow more responses
        return best_match
    return ""  # Return empty if no match found

def get_pdf_content(pdf_id: int) -> str:
    conn = get_db_connection()
    cursor = conn.cursor()
    cursor.execute("SELECT content FROM documents WHERE id = ?", (pdf_id,))
    row = cursor.fetchone()
    close_db(conn)
    return row["content"] if row else None




def get_intent_by_submenu_option(submenu_option: str) -> int:
    conn = get_db_connection()
    try:
        cursor = conn.cursor()
        cursor.execute('SELECT intent_id FROM submenu_responses WHERE submenu_option = ?', (submenu_option,))
        row = cursor.fetchone()
        return row[0] if row else None
    finally:
        close_db(conn)

def get_intent_by_id(intent_id: int) -> dict:
    conn = get_db_connection()
    try:
        cursor = conn.cursor()
        cursor.execute('SELECT * FROM intents WHERE id = ?', (intent_id,))
        row = cursor.fetchone()
        return dict(row) if row else None
    finally:
        close_db(conn)

def get_submenu_options(intent_id: int) -> List[str]:
    conn = get_db_connection()
    try:
        cursor = conn.cursor()
        cursor.execute('SELECT submenu_option FROM submenu_responses WHERE intent_id = ?', (intent_id,))
        rows = cursor.fetchall()
        return [row[0] for row in rows]
    finally:
        close_db(conn)

def get_all_submenu_options() -> List[Tuple[str]]:
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

def update_keyword_in_db(keyword_id, new_keyword, new_priority):
    """Update the keyword text and priority of an existing keyword."""
    conn = get_db_connection()
    try:
        cursor = conn.cursor()
        cursor.execute('UPDATE keywords SET keyword = ?, priority = ? WHERE id = ?', (new_keyword, new_priority, keyword_id))
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




def save_feedback(user_message, bot_message, feedback):
    conn = get_db_connection()
    try:
        cursor = conn.cursor()
        cursor.execute('''
            INSERT INTO feedback (user_message, bot_response, feedback)
            VALUES (?, ?, ?)
        ''', (user_message, bot_message, feedback))
        conn.commit()
    finally:
        close_db(conn)

def get_feedback_from_db():
    conn = get_db_connection()
    try:
        cursor = conn.cursor()
        cursor.execute('SELECT * FROM feedback')
        rows = cursor.fetchall()
        return [dict(row) for row in rows]
        
    finally:
        close_db(conn)
        
def delete_feedback_from_db(feedback_id):
    """Delete a feedback entry from the database."""
    conn = get_db_connection()
    try:
        cursor = conn.cursor()
        cursor.execute('DELETE FROM feedback WHERE id = ?', (feedback_id,))
        conn.commit()
        return cursor.rowcount > 0  # Returns True if a row was deleted
    finally:
        close_db(conn)




def extract_text_from_pdf(pdf_file) -> str:
    pdf_text = ""
    pdf_file.stream.seek(0)  # Move to the start of the file
    pdf_data = pdf_file.read()  # Read file content into bytes

    # Use the byte stream with fitz.open() to open the PDF
    with fitz.open(stream=pdf_data, filetype="pdf") as pdf:
        for page_num in range(pdf.page_count):
            page = pdf[page_num]
            pdf_text += page.get_text("text")

    return pdf_text

def save_pdf_to_db(filename: str, content: str) -> int:
    conn = get_db_connection()
    cursor = conn.cursor()
    cursor.execute("INSERT INTO documents (filename, content) VALUES (?, ?)", (filename, content))
    conn.commit()
    pdf_id = cursor.lastrowid
    close_db(conn)
    return pdf_id


