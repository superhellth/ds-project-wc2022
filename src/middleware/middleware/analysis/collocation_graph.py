from collections import defaultdict
import json
import ast
import itertools
import networkx as nx
import matplotlib.pyplot as plt

class CollocationGraphGenerator:
    """This class generates collocation graphs using the collocations files."""

    def to_dict_of_dicts(self, string_dict):
        dict_of_dicts = defaultdict(dict)
        for entry in string_dict.items():
            key_tuple = ast.literal_eval(entry[0])
            dict_of_dicts[key_tuple[0]][key_tuple[1]] = {"weight": entry[1]}
        return dict_of_dicts

    def generate_graph(self, window_size, path_to_files):
        """Generate collocation graph with given window size."""
        f = open(path_to_files + "collocations" + str(window_size) + ".json", "r", encoding="utf_8")
        print("Loading file...")
        edge_dict = json.loads(f.read())
        print("Done!")
        edge_dict = dict(itertools.islice(edge_dict.items(), 1000))
        print("Converting dict to dict of dicts")
        edge_dict = self.to_dict_of_dicts(edge_dict)
        print("Done!")

        G = nx.from_dict_of_dicts(edge_dict)
        pos = nx.spring_layout(G)

        # set coordinates of node, necessary for graphology to read it
        for node in G.nodes:
            G.nodes[node]["x"] = pos[node][0]
            G.nodes[node]["y"] = pos[node][1]

        nx.write_gexf(G, path_to_files + "collocations" + str(window_size) + ".gexf")

graph_generator = CollocationGraphGenerator()
graph_generator.generate_graph(3, path_to_files="./src/data/")
