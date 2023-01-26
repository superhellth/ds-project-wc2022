import ujson
from middleware.analysis import nlp_support
from middleware.analysis import collocation_graph

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

graph_builder = collocation_graph.CollocationGraphGenerator("./src/data/", "./src/data/word-graph/")
graph_builder.generate_and_cluster(0, 2000, False, 2, 100, "k-means", 8, False, True)
