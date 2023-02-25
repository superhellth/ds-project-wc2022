import json
import os
from wordcloud import WordCloud
from collections import Counter
import spacy

custom_stop_words = {"<link>","link","live","stream"}

nlp = spacy.load('en_core_web_sm')
spacy_stop_words = nlp.Defaults.stop_words

stop_words = spacy_stop_words.union(custom_stop_words)

# Open the json file and load its contents
file_path = os.path.join('C:\\Users\\rapha\\Desktop\\Fünftes Semester\\DataScience\\i_grams_json\\', 'bigrams.json')

with open(file_path, 'r') as f:
    ngrams = json.loads(f.read())

#unigrams_filtered = {word: count for word, count in ngrams.items() if word.lower() not in stop_words}

filtered_ngrams = {}
i = 0
for key, value in ngrams.items():
    if i<5:
        #new_key = "{key[0]} {key[1]}"
        #filtered_ngrams[new_key] = value
        new_key = key.replace("'", "").replace("(", "").replace(")", "").replace(",", " ").upper()
        filtered_ngrams[new_key] = value

filtered_strings = {}
for key, value in filtered_ngrams.items():
    words = key.split()
    if not any(w.lower() in stop_words for w in words) and any(ord(c) < 128 for c in words):
        filtered_strings[key] = filtered_ngrams[key]

wordcloud = WordCloud()


score = Counter(filtered_strings)
wordcloud.generate_from_frequencies(score)
wordcloud.to_file("wordcloud_bigrams_filtered.png")