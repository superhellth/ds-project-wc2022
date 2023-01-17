from collections import defaultdict
import json
import ast
import itertools
import networkx as nx
import spacy
from middleware.analysis import stat_provider

class CollocationGraphGenerator:
    """This class generates collocation graphs using the collocations files."""

    def __init__(self, path_to_data_files):
        self.nlp = spacy.load("en_core_web_sm")
        self.stat_provider = stat_provider.StatProvider(path_to_data_files)

    def to_dict_of_dicts(self, string_dict, include_stop_word_nodes=True):
        """Converts dict to dict of dicts for networkx to be able to convert it to a graph."""
        dict_of_dicts = defaultdict(dict)
        for entry in string_dict.items():
            key_tuple = ast.literal_eval(entry[0])
            if include_stop_word_nodes or (key_tuple[0] not in self.nlp.Defaults.stop_words and key_tuple[1] not in self.nlp.Defaults.stop_words):
                dict_of_dicts[key_tuple[0]][key_tuple[1]] = {"weight": entry[1]}
        return dict_of_dicts

    def generate_graph(self, window_size, num_edges=-1, include_stop_word_nodes=True):
        """Generate collocation graph with given window size."""
        print("Loading collocation counts...")
        edge_dict = self.stat_provider.get_collocations_as_list(window_size)[:num_edges]
        print("Done!")
        edge_dict = {entry[0]: entry[1] for entry in edge_dict}
        print("Converting dict to dict of dicts")
        edge_dict = self.to_dict_of_dicts(edge_dict, include_stop_word_nodes=include_stop_word_nodes)
        print("Done!")

        G = nx.from_dict_of_dicts(edge_dict)
        pos = nx.spring_layout(G)

        # set coordinates of node, necessary for graphology to read it
        for node in G.nodes:
            G.nodes[node]["x"] = pos[node][0]
            G.nodes[node]["y"] = pos[node][1]

        return G

graph_generator = CollocationGraphGenerator(path_to_data_files="./src/data/")
graph = graph_generator.generate_graph(2, num_edges=10000, include_stop_word_nodes=False)
nx.write_gexf(graph, "./src/data/collocations2nostop.gexf")
