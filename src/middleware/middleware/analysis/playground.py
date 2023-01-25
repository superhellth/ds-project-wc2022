import ujson
from middleware.analysis import nlp_support
from middleware.analysis import common_words
from middleware.analysis import tf_idf_calculator
import numpy as np

corpus_counter = nlp_support.CorpusAnalyzer()

COLLOCATIONS2_FILE = "./src/data/collocations2.json"
COLLOCATIONS3_FILE = "./src/data/collocations3.json"
COLLOCATIONS4_FILE = "./src/data/collocations4.json"
FOURGRAMS_FILE = "./src/data/fourgrams.json"
NES_FILE = "./src/data/nes.json"
NES_COLLOCATIONS_FILE = "./src/data/nes_collocations.json"

def write_to_file(counts, write_to: str):
    """Write the count dict to file."""
    with open(write_to, "w", encoding="utf_8") as file:
        file.write(ujson.dumps(counts))

<<<<<<< HEAD
"""tf_idf = tf_idf_calculator.TfIdfCalculator()
matrix = tf_idf.calculate_tf_idf()
print(type(matrix))"""

def get_top_n_indices(matrix, n):
    # Find the indices of the top n highest entries
    flat_indices = np.argpartition(-matrix.flatten(), n)[:n]
    # Use the indices to get the corresponding values
    top_n_values = matrix.flatten()[flat_indices]
    # Convert the indices from a flat array to multi-dimensional indices
    multi_indices = [np.unravel_index(flat_index, matrix.shape) for flat_index in flat_indices]
    return top_n_values, multi_indices

"""corpus = ["a","b","c","d","e","f"]
matrix = np.array([[1,2,6,3,5,9], [3,4,6,3,8,2],[8,6,3,7,2,4]])
top_5_values, top_5_indices = get_top_n_indices(matrix, 3)
print(top_5_values)
print(top_5_indices)
for i in range(3):
    print(top_5_values[i],corpus[top_5_indices[i][0]],corpus[top_5_indices[i][1]])"""

tf_idf = tf_idf_calculator.TfIdfCalculator()
values = tf_idf.nth_simiular_tweets(num_tweets=1500,n=10)
for i in range(len(values)):
    print(values[i])
    print("______________________________")


#collocations4 = corpus_counter.generate_collocation_counts(window_size=4)
#write_to_file(collocations4, COLLOCATIONS4_FILE)
=======
nes = corpus_counter.generate_nes_counts(num_tweets=2000)
write_to_file(nes, NES_FILE)
>>>>>>> b80b247f7c74c65b1c20f6a316144346d659e705

### Code to generate all count files ###
### Do not execute unless old files are saved or there is a good reason to regenerate ###

# # these 2 are equal
# BIGRAM_FILE = "./src/data/bigrams.json"
# COLLOCATIONS2_FILE = "./src/data/collocations2.json"

# # these are all different
# UNIGRAM_FILE = "./src/data/unigrams.json"
# TRIGRAM_FILE = "./src/data/trigrams.json"
# COLLOCATIONS3_FILE = "./src/data/collocations3.json"
# COLLOCATIONS4_FILE = "./src/data/collocations4.json"

# NUM_THREADS = 10

# # n-grams
# unigrams = corpus_counter.generate_n_grams(n=1, num_threads=NUM_THREADS)
# write_to_file(unigrams, UNIGRAM_FILE)
# bigrams = corpus_counter.generate_n_grams(n=2, num_threads=NUM_THREADS)
# write_to_file(bigrams, BIGRAM_FILE)
# trigrams = corpus_counter.generate_n_grams(n=3, num_threads=NUM_THREADS)
# write_to_file(trigrams, TRIGRAM_FILE)

# # collocations
# collocations2 = corpus_counter.generate_collocation_counts(window_size=2, num_threads=NUM_THREADS)
# write_to_file(collocations2, COLLOCATIONS2_FILE)
# collocations3 = corpus_counter.generate_collocation_counts(window_size=3, num_threads=NUM_THREADS)
# write_to_file(collocations3, COLLOCATIONS3_FILE)
# collocations4 = corpus_counter.generate_collocation_counts(window_size=4, num_threads=NUM_THREADS)
# write_to_file(collocations4, COLLOCATIONS4_FILE)
