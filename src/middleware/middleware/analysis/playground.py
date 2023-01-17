import ujson
from middleware.analysis import nlp_support

corpus_counter = nlp_support.CorpusAnalyzer()

COLLOCATIONS2_FILE = "./src/data/collocations2.json"
COLLOCATIONS3_FILE = "./src/data/collocations3.json"
COLLOCATIONS4_FILE = "./src/data/collocations4.json"

def write_to_file(counts, write_to: str):
    """Write the count dict to file."""
    with open(write_to, "w", encoding="utf_8") as file:
        file.write(ujson.dumps(counts))

collocations2 = corpus_counter.generate_collocation_counts(window_size=2)
write_to_file(collocations2, COLLOCATIONS2_FILE)

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
