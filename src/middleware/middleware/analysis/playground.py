import spacy
import re

# Load the language model
nlp = spacy.load("en_core_web_sm")

text = "This is a #darts tweet"
placeholder = "thisisauniqueandhopefullyunusedplaceholderstring"

text = re.sub(r'#', placeholder, text)

# Tokenize a string
doc = nlp(text)

tokens = [re.sub(placeholder, "#", token.text) for token in doc]

# Print the tokens
for token in tokens:
    print(token)