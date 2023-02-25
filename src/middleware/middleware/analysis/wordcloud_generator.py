import json
import os
from wordcloud import WordCloud
from collections import Counter
import spacy
import re
class WordCloudGenerator:
    """This class generates wordcloud graphics from unigrams, bigrams, trigrams and fourgrams.
    The resulting png data will be saved in the top-level folder of the project.
    The ngram.json files need to be saved first in the folder specified in the path.
    All methods have no return value, they generated png directly."""

    def generate_wordcloud_unigrams(self):
        """Generates wordcloud from unigrams. Excludes words including non-ascii characters, even placeholders for emojis etc., or custom stopwords.
        """
        #Defining the stopwords
        custom_stop_words = {"<link>", "link", "live", "stream"}
        nlp = spacy.load('en_core_web_sm')
        spacy_stop_words = nlp.Defaults.stop_words

        stop_words = spacy_stop_words.union(custom_stop_words)

        # Open the unigram json file and load its content from the specified folder
        file_path = os.path.join('C:\\Users\\rapha\\Desktop\\Fünftes Semester\\DataScience\\i_grams_json\\', 'unigrams.json')

        with open(file_path, 'r') as f:
            ngrams = json.loads(f.read())

        #Filtering the ngrams for unwanted words
        filtered_strings = {}
        for key, value in ngrams.items():
            if key.lower() not in stop_words and all(c.isalnum() and ord(c) < 128 for c in key) and not any(re.search(r'\\U0000', w) for w in words):
                filtered_strings[key] = value

        #Generate the wordcloud
        wordcloud = WordCloud()
        score = Counter(filtered_strings)
        wordcloud.generate_from_frequencies(score)
        wordcloud.to_file("wordcloud_unigrams_filtered.png")

    def generate_wordcloud_bigrams(self):
        """Generates wordcloud from bigrams. Excludes words including non-ascii characters, even placeholders for emojis etc., or custom stopwords.
        """

        #Defining the stopwords
        custom_stop_words = {"<link>","link","live","stream"}
        nlp = spacy.load('en_core_web_sm')
        spacy_stop_words = nlp.Defaults.stop_words
        stop_words = spacy_stop_words.union(custom_stop_words)

        # Open the unigram json file and load its content from the specified folder
        file_path = os.path.join('C:\\Users\\rapha\\Desktop\\Fünftes Semester\\DataScience\\i_grams_json\\', 'bigrams.json')

        with open(file_path, 'r') as f:
            ngrams = json.loads(f.read())

        #Change the ngrams from their tupel representation to a capatilized string representation
        filtered_ngrams = {}
        for key, value in ngrams.items():
            new_key = key.replace("'", "").replace("(", "").replace(")", "").replace(",", " ").upper()
            filtered_ngrams[new_key] = value

        #Filtering the ngrams for unwanted words
        filtered_strings = {}
        for key, value in filtered_ngrams.items():
            words = key.split()
            if not any(w.lower() in stop_words for w in words) and not any(re.search(r'\\U0000', w) for w in words) and all(w.isalnum() and all(ord(c) < 128 for c in w) for w in words):
                filtered_strings[key] = filtered_ngrams[key]

        #Generate the wordcloud
        wordcloud = WordCloud()
        score = Counter(filtered_strings)
        wordcloud.generate_from_frequencies(score)
        wordcloud.to_file("wordcloud_bigrams_filtered.png")
        

    def generate_wordcloud_trigrams(self):
        """Generates wordcloud from trigrams. Excludes tupels either including non-ascii characters, even placeholders for emojis etc., or custom stopwords.
        """

        #Defining the stopwords
        custom_stop_words = {"<link>", "link", "live", "stream"}
        nlp = spacy.load('en_core_web_sm')
        spacy_stop_words = nlp.Defaults.stop_words
        stop_words = spacy_stop_words.union(custom_stop_words)

        # Open the unigram json file and load its content from the specified folder
        file_path = os.path.join('C:\\Users\\rapha\\Desktop\\Fünftes Semester\\DataScience\\i_grams_json\\', 'trigrams.json')

        with open(file_path, 'r') as f:
            ngrams = json.loads(f.read())

        #Change the ngrams from their tupel representation to a capatilized string representation
        filtered_ngrams = {}
        for key, value in ngrams.items():
            new_key = key.replace("'", "").replace("(", "").replace(")", "").replace(",", " ").upper()
            filtered_ngrams[new_key] = value

        #Filtering the ngrams for unwanted words
        filtered_strings = {}
        for key, value in filtered_ngrams.items():
            words = key.split(" ")
            if not any(w.lower() in stop_words for w in words) and all(w.isalnum() or all(ord(c) < 128 for c in w) for w in words):
                filtered_strings[key] = filtered_ngrams[key]

        #Generate the wordcloud
        wordcloud = WordCloud()
        score = Counter(filtered_strings)
        wordcloud.generate_from_frequencies(score)
        wordcloud.to_file("wordcloud_trigrams_filtered.png")

    def generate_wordcloud_fourgrams(self):
        """Generates wordcloud from fourgrams. Excludes tupels either including non-ascii characters, even placeholders for emojis etc., or custom stopwords.
        """

        #Defining the stopwords
        custom_stop_words = {"<link>", "link", "live", "stream"}
        nlp = spacy.load('en_core_web_sm')
        spacy_stop_words = nlp.Defaults.stop_words
        stop_words = spacy_stop_words.union(custom_stop_words)

        # Open the unigram json file and load its content from the specified folder
        file_path = os.path.join('C:\\Users\\rapha\\Desktop\\Fünftes Semester\\DataScience\\i_grams_json\\', 'fourgrams.json')

        with open(file_path, 'r') as f:
            ngrams = json.loads(f.read())

        #Change the ngrams from their tupel representation to a capatilized string representation
        filtered_ngrams = {}
        for key, value in ngrams.items():
            new_key = key.replace("'", "").replace("(", "").replace(")", "").replace(",", " ").upper()
            filtered_ngrams[new_key] = value

        #Filtering the ngrams for unwanted words
        filtered_strings = {}
        for key, value in filtered_ngrams.items():
            words = key.split(" ")
            if not any(w.lower() in stop_words for w in words) and all(w.isalnum() or all(ord(c) < 128 for c in w) for w in words):
                filtered_strings[key] = filtered_ngrams[key]

        #Generate the wordcloud
        wordcloud = WordCloud()
        score = Counter(filtered_strings)
        wordcloud.generate_from_frequencies(score)
        wordcloud.to_file("wordcloud_fourgrams_filtered.png")