from flask import Flask, render_template, request, jsonify
import fitz  # PyMuPDF
import sqlite3
import io
from utils import (
    handle_input,
    get_intents_from_db, 
    add_intent_to_db, 
    update_intent_in_db, 
    delete_intent_from_db,
    get_responses_from_db,
    add_response_to_db,
    update_response_in_db,
    delete_response_from_db,
    get_keywords_from_db,
    add_keyword_to_db,
    update_keyword_in_db,
    delete_keyword_from_db,
    get_submenu_responses_from_db,
    add_submenu_response_to_db,
    update_submenu_response_in_db,
    delete_submenu_response_from_db,
    save_feedback,
    get_feedback_from_db,
    delete_feedback_from_db,
    extract_text_from_pdf,
    save_pdf_to_db
    
)
DATABASE = 'database.db'
def get_db_connection():
    conn = sqlite3.connect(DATABASE)
    conn.row_factory = sqlite3.Row  # This allows rows to be returned as dictionaries
    return conn

app = Flask(__name__, 
            template_folder="../frontend/templates",
            static_folder="../frontend",
            static_url_path='')

@app.route('/')
def index():
    return render_template('index.html')

@app.route('/database')
def database_management():
    return render_template('database.html')


@app.route('/feedback_management')
def feedbackmanagement():
    return render_template('feedback_management.html')

@app.route('/upload')
def uploadpdf():
    return render_template('upload.html')

@app.route('/chat', methods=['POST'])
def chat():
    user_message = request.json.get('message')
    response_data = handle_input(user_message)
    return jsonify(response_data)

# Intents management
@app.route('/intents', methods=['GET'])
def get_intents():
    intents = get_intents_from_db()
    return jsonify(intents)

@app.route('/intents/add', methods=['POST'])
def add_intent():
    data = request.json
    intent_name = data.get('intent_name')
    has_submenu = data.get('has_submenu')
    success = add_intent_to_db(intent_name, has_submenu)
    return jsonify({'success': success})

@app.route('/intents/update', methods=['POST'])
def update_intent():
    data = request.json
    intent_id = data.get('id')
    intent_name = data.get('intent_name')
    has_submenu = data.get('has_submenu')
    success = update_intent_in_db(intent_id, intent_name, has_submenu)
    return jsonify({'success': success})

@app.route('/intents/delete', methods=['POST'])
def delete_intent():
    data = request.json
    intent_id = data.get('id')
    success = delete_intent_from_db(intent_id)
    return jsonify({'success': success})

# Responses management
@app.route('/responses', methods=['GET'])
def get_responses():
    responses = get_responses_from_db()
    return jsonify(responses)

@app.route('/responses/add', methods=['POST'])
def add_response():
    data = request.json
    intent_id = data.get('intent_id')
    response = data.get('response')
    success = add_response_to_db(intent_id, response)
    return jsonify({'success': success})

@app.route('/responses/update', methods=['POST'])
def update_response():
    data = request.json
    response_id = data.get('id')
    response = data.get('response')
    
    # Call the updated function that only updates the response text
    success = update_response_in_db(response_id, response)
    
    return jsonify({'success': success})


@app.route('/responses/delete', methods=['POST'])
def delete_response():
    data = request.json
    response_id = data.get('id')
    success = delete_response_from_db(response_id)
    return jsonify({'success': success})

# Keywords management
@app.route('/keywords', methods=['GET'])
def get_keywords():
    keywords = get_keywords_from_db()
    return jsonify(keywords)

@app.route('/keywords/add', methods=['POST'])
def add_keyword():
    data = request.json
    intent_id = data.get('intent_id')
    keyword = data.get('keyword')
    success = add_keyword_to_db(intent_id, keyword)
    return jsonify({'success': success})

@app.route('/keywords/update', methods=['POST'])
def update_keyword():
    data = request.json
    keyword_id = data.get('id')
    new_keyword = data.get('keyword')
    new_priority = data.get('priority')
    
    if not keyword_id or not new_keyword or new_priority is None:
        return jsonify({'success': False, 'message': 'Invalid input.'}), 400
    
    success = update_keyword_in_db(keyword_id, new_keyword, new_priority)
    return jsonify({'success': success})


@app.route('/keywords/delete', methods=['POST'])
def delete_keyword():
    data = request.json
    keyword_id = data.get('id')
    success = delete_keyword_from_db(keyword_id)
    return jsonify({'success': success})

# Submenu Responses management
@app.route('/submenu_responses', methods=['GET'])
def get_submenu_responses():
    submenu_responses = get_submenu_responses_from_db()
    return jsonify(submenu_responses)

@app.route('/submenu_responses/add', methods=['POST'])
def add_submenu_response():
    data = request.json
    intent_id = data.get('intent_id')
    submenu_option = data.get('submenu_option')
    submenu_response = data.get('submenu_response')
    success = add_submenu_response_to_db(intent_id, submenu_option, submenu_response)
    return jsonify({'success': success})

@app.route('/submenu_responses/update', methods=['POST'])
def update_submenu_response():
    data = request.json
    submenu_response_id = data.get('id')
    
    submenu_option = data.get('submenu_option')
    submenu_response = data.get('submenu_response')
    success = update_submenu_response_in_db(submenu_response_id, submenu_option, submenu_response)
    return jsonify({'success': success})

@app.route('/submenu_responses/delete', methods=['POST'])
def delete_submenu_response():
    data = request.json
    submenu_response_id = data.get('id')
    success = delete_submenu_response_from_db(submenu_response_id)
    return jsonify({'success': success})

@app.route('/store_feedback', methods=['POST'])
def store_feedback():
    data = request.json
    user_message = data.get('user_message')
    bot_message = data.get('bot_message')
    feedback = data.get('feedback')

    # Ensure feedback data was received
    if not all([user_message, bot_message, feedback]):
        return jsonify({"error": "Missing data"}), 400

    # Save feedback data using the renamed save_feedback function
    try:
        save_feedback(user_message, bot_message, feedback)
        return jsonify({"message": "Feedback saved successfully"}), 200
    except Exception as e:
        print(f"Error saving feedback: {e}")
        return jsonify({"error": "Failed to save feedback"}), 500
    

@app.route('/feedback', methods=['GET'])
def get_feedback():
    feedback=get_feedback_from_db()
    return jsonify(feedback)

# Delete feedback entry
@app.route('/feedback/delete', methods=['POST'])
def delete_feedback():
    data = request.json
    feedback_id = data.get('id')
    
    if feedback_id is None:
        return jsonify({'success': False, 'message': 'Invalid ID provided.'}), 400

    success = delete_feedback_from_db(feedback_id)
    return jsonify({'success': success})






@app.route('/upload_pdf', methods=['POST'])
def upload_pdf():
    file = request.files['file']
    
    if not file or not file.filename.endswith('.pdf'):
        return jsonify({"error": "Invalid file format. Please upload a PDF."}), 400

    # Extract text from PDF
    pdf_text = extract_text_from_pdf(file)

    # Save document and content in the database
    pdf_id = save_pdf_to_db(file.filename, pdf_text)

    return jsonify({"message": "PDF uploaded successfully.", "pdf_id": pdf_id})



@app.route('/get_similar_questions', methods=['POST'])
def get_similar_questions():
    conn = get_db_connection()
    cursor = conn.cursor()
    cursor.execute('SELECT similar_question FROM similar_questions')
    rows = cursor.fetchall()
    conn.close()

    # Ensure the rows are returned as dictionaries
    similar_questions = [row['similar_question'] for row in rows]
    
    print(similar_questions)  # Log the output to see the similar questions

    return jsonify(similar_questions)


    

if __name__ == "__main__":
    app.run(debug=True)
