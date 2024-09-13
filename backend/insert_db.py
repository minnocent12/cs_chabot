# insert_data.py

import sqlite3

# Connect to SQLite database
conn = sqlite3.connect('database.db')
cursor = conn.cursor()

# Insert intents and associated data
intents_data = [
    ('general', False),
    ('research', False),
    ('conduct', False),
    ('admission', True),
    ('degrees', False),
    ('academic', False),
    ('conflicts', False)
]

cursor.executemany('INSERT INTO intents (intent_name, has_submenu) VALUES (?, ?)', intents_data)

# Insert keywords 
keywords_data = [
    (1, 'general'), (1, 'course information'), (1, 'what courses are offered'), (1, 'What graduate programs does the Computer Science Department offer?'),
    (1, 'What degrees are offered by the Computer Science Department?'),
    (2, 'research'), (2, 'research areas'), (2, 'What are the research areas in the Computer Science Department?'), (2, 'What research areas are emphasized in the Computer Science Department?'),
    (3, 'conduct'), (3, 'Code of Conduct'), (3, 'What is the Student Code of Conduct?'),
    (4, 'admission'), (4, 'admission process'), (4, 'application requirements'), (4, 'how to apply'),
    (5, 'degrees'), (5, 'program'),  (5, 'programs'), (5, 'degree'),
    (6, 'academic'), (6, 'Who handles academic and non-academic misconduct?'), (6, 'misconduct'),
    (7, 'conflicts'),  (7, 'What should I do if I have a conflict with my advisor?'),  (7, 'misunderstanding')
]
cursor.executemany('INSERT INTO keywords (intent_id, keyword) VALUES (?, ?)', keywords_data)

# Insert responses
responses_data = [
    (1, 'The Department of Computer Science offers several advanced degree programs. Students can pursue an M.S. in Computer Science with concentrations in Computer Science, Bioinformatics, or Security and Privacy. Additionally, there is an M.S. in Data Science and Analytics with a focus on Big Data and Machine Learning (BDML). For those seeking a research-oriented path, the department offers a Ph.D. in Computer Science with concentrations in Computer Science or Bioinformatics. The faculty are deeply involved in a range of research areas including artificial intelligence, mobile systems, bioinformatics, databases, digital image and signal processing, graphics, networks, and software engineering.'),
    (2, 'Faculty in the Computer Science Department engage in a broad array of research endeavors. These include artificial intelligence and neural networks, mobile systems and robotics, bioinformatics, databases, digital image and signal processing, graphics and visualization, networks, parallel and distributed computing, programming languages, simulation and modeling, and software engineering.'),
    (3, 'The Student Code of Conduct sets forth the University’s expectations for student behavior and their rights. It provides a framework for both academic and non-academic conduct and is designed to promote an environment conducive to academic excellence. The Dean of Students Office is responsible for administering and overseeing the Code of Conduct.'),
    (4, 'Here is information about admission...'),
    (5, 'The Computer Science Department offers the following degrees...'),
    (6, 'The Dean of Students Office oversees the administration of the Student Code of Conduct. This includes handling both academic and non-academic misconduct cases.'),
    (7, 'If you are a Ph.D. or M.S. thesis student and encounter difficulties communicating with your advisor or resolving conflicts, the staff is available to assist you. They can help facilitate effective communication or arrange mediated conversations. It’s advisable to seek assistance as soon as a problem arises to prevent escalation.')
]
cursor.executemany('INSERT INTO responses (intent_id, response) VALUES (?, ?)', responses_data)

# Insert submenu options for "admission"
submenu_responses_data = [
    (4, 'Undergraduate Admission', 'The undergraduate admission process includes...'),
    (4, 'Graduate Admission', 'The graduate admission process includes...')
]
cursor.executemany('INSERT INTO submenu_responses (intent_id, submenu_option, submenu_response) VALUES (?, ?, ?)', submenu_responses_data)

# Commit and close
conn.commit()
conn.close()

print("Data inserted successfully.")
