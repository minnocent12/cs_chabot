import spacy

# Load the spaCy model
nlp = spacy.load("en_core_web_sm")

def is_cs_related(user_input):
    doc = nlp(user_input)
    # Example: Check for named entities related to the CS department
    for ent in doc.ents:
        if ent.label_ in ["ORG", "GPE"] and "computer science" in ent.text.lower():
            return True
    return False
