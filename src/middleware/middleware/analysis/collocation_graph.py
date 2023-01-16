from collections import defaultdict
import json
import ast
import itertools
import networkx as nx
import spacy
import matplotlib.pyplot as plt

class CollocationGraphGenerator:
    """This class generates collocation graphs using the collocations files."""

    def __init__(self):
        self.nlp = spacy.load("en_core_web_sm")

    def to_dict_of_dicts(self, string_dict, include_stop_word_nodes=True):
        """Converts dict to dict of dicts for networkx to be able to convert it to a graph."""
        dict_of_dicts = defaultdict(dict)
        for entry in string_dict.items():
            key_tuple = ast.literal_eval(entry[0])
            if include_stop_word_nodes or (key_tuple[0] not in self.nlp.Defaults.stop_words and key_tuple[1] not in self.nlp.Defaults.stop_words):
                dict_of_dicts[key_tuple[0]][key_tuple[1]] = {"weight": entry[1]}
        return dict_of_dicts

    def generate_graph(self, window_size, path_to_files, num_edges=-1, include_stop_word_nodes=True):
        """Generate collocation graph with given window size."""
        f = open(path_to_files + "collocations" + str(window_size) + ".json", "r", encoding="utf_8")
        print("Loading file...")
        edge_dict = json.loads(f.read())
        print("Done!")
        if num_edges != -1:
            edge_dict = dict(itertools.islice(edge_dict.items(), num_edges))
        print("Converting dict to dict of dicts")
        edge_dict = self.to_dict_of_dicts(edge_dict, include_stop_word_nodes=include_stop_word_nodes)
        print("Done!")

        G = nx.from_dict_of_dicts(edge_dict)
        pos = nx.spring_layout(G)
        # plt.show()

        # set coordinates of node, necessary for graphology to read it
        for node in G.nodes:
            G.nodes[node]["x"] = pos[node][0]
            G.nodes[node]["y"] = pos[node][1]

        nx.write_gexf(G, path_to_files + "collocations" + str(window_size) + ".gexf")

graph_generator = CollocationGraphGenerator()
graph_generator.generate_graph(3, path_to_files="./src/data/", num_edges=10000, include_stop_word_nodes=False)
