Computer Science Department Chatbot
This project is a rule-based and hybrid chatbot specifically designed to answer questions related to the Computer Science department at a Georgia State university. The chatbot can handle both predefined questions and more open-ended queries using a combination of keyword detection, machine learning (Natural language Processing).

Features
Predefined Questions: The chatbot handles predefined questions covering topics such as courses, admission, program details, eligibility, graduation requirements, and career opportunities.
Natural Language Processing: For non-predefined queries related to the Computer Science department, the chatbot uses NLP techniques to detect and classify user intents.
Web Interface: A frontend interface with a chatbot widget that users can interact with directly.

Project Structure

cs_chatbot/
├── backend/
│   ├── app.py                  # Main backend script
│   ├── intent_classifier.py    # Intent classification logic
│   ├── intents.py              # Handles loading intents from the database
│   ├── responses.py            # Fetches responses for intents
│   └── utils.py                # Utility functions
├── frontend/
│   ├── assets/
│   │   ├── logo.png            # Logo image
│   │   ├── chat.png            # Chat-related assets
│   │   └── [other images]
│   ├── templates/
│   │   └── index.html          # Frontend HTML template
│   ├── chat.js                 # Frontend JavaScript logic
│   └── style.css               # Frontend styles
├── database.db                 # SQLite database file
├── README.md                   # Documentation
└── requirements.txt            # Python dependencies



Installation


Clone the Repository:
Open terminal and navigate to the folder you want to locate the project and then run the following commands:

git clone git@github.com:minnocent12/cs_chabot.git
cd cs_chabot 
rm -rf .git 

Zipped the file:
Download the zip the file and place it into the directory you would like to place your project, then unzip the file, then run the following command:
cd cs_chabot
rm -rf .git 
Set up a Virtual Environment after clone the repository or zip the file:

python3 -m venv venv

.\venv\Scripts\activate  (to activate the environment in windows OS)

source venv/bin/activate  (to activate the environment in Mac OS)

Install the Dependencies:

pip install -r requirements.txt
If your pip is outdated run this command: pip install --upgrade pip

# After installation of dependencies and updating pip, run the following command to install Natural Language Processing large Mode: 
python -m spacy download en_core_web_lg

then run:

python3 backend/app.py

Access the Web Interface:

Open a browser and go to http://127.0.0.1:5000 to interact with the chatbot.

Usage

Click on the chat icon at the bottom-right corner of the webpage to initiate a conversation with the bot.
You can ask predefined questions using buttons like "What programs are offered by the Computer Science Department?
" or "What should I do if a class is full?"

For open-ended questions, simply type your question, and the chatbot will either match it to an intent or generate a response similarity matching.

Technologies Used

Flask: Web framework for the backend server.
JavaScript (chat.js): Manages the frontend chatbot interaction.
CSS (style.css): Styling for the chatbot widget.
spacy: Used for intent classification (NLP model).

Contributing
Contributions are welcome! Feel free to fork the repository and submit pull requests.

License
This project is licensed under the INNOSTAR License.

