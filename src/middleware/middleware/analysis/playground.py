import ujson
from middleware.analysis import nlp_support

def write_to_file(counts, write_to: str):
    """Write the count dict to file."""
    with open(write_to, "w", encoding="utf_8") as file:
        file.write(ujson.dumps(counts))

corpus_analyzer = nlp_support.CorpusAnalyzer()

ne_collocations = corpus_analyzer.generate_nes_collocation_counts(num_tweets=1000)

write_to_file(ne_collocations, "./src/data/nes_collocations.json")
