from flask import Flask, render_template, request, jsonify
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
    delete_submenu_response_from_db
)

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

if __name__ == "__main__":
    app.run(debug=True)
