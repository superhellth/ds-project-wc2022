import ujson
from middleware.analysis import nlp_support

def write_to_file(counts, write_to: str):
    """Write the count dict to file."""
    with open(write_to, "w", encoding="utf_8") as file:
        file.write(ujson.dumps(counts))

corpus_analyzer = nlp_support.CorpusAnalyzer()

ne_collocations = corpus_analyzer.generate_collocation_counts(window_size=4, num_threads=8, batch_size=10000)

write_to_file(ne_collocations, "./../../../../src/data/collocations4.json")
