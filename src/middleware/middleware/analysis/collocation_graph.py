from collections import defaultdict
import ast
import numpy as np
import networkx as nx
from sklearn.cluster import KMeans
import spacy
from node2vec import Node2Vec
from middleware.analysis import stat_provider

class CollocationGraphGenerator:
    """This class generates collocation graphs using the collocations files."""

    def __init__(self, path_to_data_files, path_to_graph_files):
        self.nlp = spacy.load("en_core_web_sm")
        self.stat_provider = stat_provider.StatProvider(path_to_data_files)
        self.path_to_graph_files = path_to_graph_files
        self.colors = ["#FF0000", "#FF8000", "#F3FF00", "#00FF01", "#00FFED", "#0008FF", "#BF00FF", "#FF00C9", "#FF0000", "#000000", "#808080", "#004A08", "#6F0000", "#00466F", "#57006F"]

    def to_dict_of_dicts(self, string_dict, include_stop_word_nodes=True, min_node_length=1):
        """Converts dict to dict of dicts for networkx to be able to convert it to a graph."""
        stop_words = list(self.nlp.Defaults.stop_words) + ["<link>"]
        dict_of_dicts = defaultdict(dict)
        for entry in string_dict.items():
            key_tuple = ast.literal_eval(entry[0])
            if include_stop_word_nodes or (key_tuple[0] not in stop_words and key_tuple[1] not in stop_words):
                if len(key_tuple[0]) >= min_node_length and len(key_tuple[1]) >= min_node_length:
                    dict_of_dicts[key_tuple[0]][key_tuple[1]] = {"weight": entry[1]}
        return dict_of_dicts

    def generate_graph(self, window_size, num_edges, include_stop_word_nodes, min_node_length):
        """Generate graph with given parameters. Applies spring layout."""
        print("Loading collocation counts...")
        edge_dict = self.stat_provider.get_collocations_as_list(window_size)[:num_edges]
        edge_dict = {entry[0]: entry[1] for entry in edge_dict}
        print("Converting dict to dict of dicts...")
        edge_dict = self.to_dict_of_dicts(edge_dict, include_stop_word_nodes=include_stop_word_nodes, min_node_length=min_node_length)
        graph = nx.from_dict_of_dicts(edge_dict)
        print("Calculating spring layout...")
        pos = nx.spring_layout(graph)
        sub_graphs = nx.connected_components(graph)
        to_remove = set()
        for sub_graph in sub_graphs:
            if len(sub_graph) < 10:
                to_remove = to_remove | sub_graph
        graph.remove_nodes_from(to_remove)
        print("Labeling nodes...")
        for node in graph.nodes:
            graph.nodes[node]["x"] = pos[node][0]
            graph.nodes[node]["y"] = pos[node][1]
            degree = len(graph.edges(node))
            total_weight = 0
            for edge in graph.edges(node):
                total_weight += graph.edges[edge]["weight"]
            graph.nodes[node]["degree"] = degree
            graph.nodes[node]["weigth"] = total_weight
            graph.nodes[node]["color"] = "grey"
        return graph

    def get_graph(self, window_size, num_edges=100, include_stop_word_nodes=True, min_node_length=1):
        """Read graph file. If not exists: generate graph."""
        unclusterd_graph_file = "unclustered_windowsize=" + str(window_size) + "_edges=" + str(num_edges) + "_includestop=" + str(include_stop_word_nodes) + "_minnodelength=" + str(min_node_length) + ".gexf"
        try:
            print("Reading graph from file...")
            G = nx.read_gexf(self.path_to_graph_files + unclusterd_graph_file)
        except FileNotFoundError:
            print("Graph file does not exists yet. Generating it...")
            G = graph_generator.generate_graph(window_size=window_size, num_edges=num_edges, include_stop_word_nodes=include_stop_word_nodes, min_node_length=min_node_length)
            nx.write_gexf(G, self.path_to_graph_files + unclusterd_graph_file)
        return G

    def learn_node2vec(self, graph: nx.Graph, embedding_size=128):
        """Generate a node2vec embedding for the given graph."""
        node2vec = Node2Vec(graph, dimensions=embedding_size, workers=4)
        print("Learning embedding...")
        return node2vec.fit(window=10, min_count=1)

    def cluster_k_means(self, graph: nx.Graph, loaded_embedding, n_cluster=8):
        """Cluster the given graph using the k-means algorithm."""
        print("Clustering using k-means...")
        X = loaded_embedding
        X = X[X[:,0].argsort()]
        Z = X[0:X.shape[0],1:X.shape[1]] # remove the node index from X and save in Z

        kmeans = KMeans(n_clusters=n_cluster, random_state=0).fit(Z) # apply kmeans on Z
        node_clusters = kmeans.labels_  # get the cluster labels of the nodes.
        node_to_label = dict(zip(X[:,0], node_clusters))

        # Iterate through the clusters and color the nodes accordingly
        for i in range(n_cluster):
            cluster_color = self.colors[i % len(self.colors)]
            cluster_nodes = [node for node in graph.nodes if node in node_to_label.keys() and node_to_label[node] == i]
            for node in cluster_nodes:
                graph.nodes[node]["color"] = cluster_color
        return graph

    def cluster_girvan_newman(self, graph: nx.Graph, min_cluster_size=10):
        """Cluster the given graph using the girvan newman algorithm."""
        print("Clustering using girvan-newman...")
        communities_generator = nx.algorithms.community.girvan_newman(graph)
        top_level_communities = next(communities_generator)

        for community in top_level_communities:
            if len(community) < min_cluster_size:
                for node in community:
                    graph.remove_node(node)
        graph.remove_nodes_from(list(nx.isolates(graph)))

        for i, community in enumerate(top_level_communities):
            if len(community) < min_cluster_size:
                continue
            community_color = self.colors[i % len(self.colors)]
            for node in community:
                graph.nodes[node]["color"] = community_color

        return graph

    def color_edges(self, graph: nx.Graph):
        """Color edges between nodes of the same color with the according color."""
        for (u, v) in graph.edges():
            if graph.nodes[u]["color"] == graph.nodes[v]["color"]:
                graph.edges[(u, v)]["color"] = graph.nodes[v]["color"]
        return graph

PATH_TO_DATA_FILES = "./src/data/"
PATH_TO_GRAPH_FILES = PATH_TO_DATA_FILES + "word-graph/"
graph_generator = CollocationGraphGenerator(path_to_data_files=PATH_TO_DATA_FILES, path_to_graph_files=PATH_TO_GRAPH_FILES)
G = graph_generator.get_graph(window_size=3, num_edges=100000, include_stop_word_nodes=False, min_node_length=2)
# model = graph_generator.learn_node2vec(G)
# model.wv.save_word2vec_format(PATH_TO_GRAPH_FILES + "embedding100000.emb")
embedding50000 = np.loadtxt(PATH_TO_GRAPH_FILES + "embedding100000.emb", skiprows=1, dtype=str, encoding="utf_8", delimiter=" ", comments=None)
G = graph_generator.cluster_k_means(G, embedding50000, n_cluster=11)
nx.write_gexf(G, "./src/data/word-graph/collocations3_top100000_nostop_min2nodelength_kmeans11.gexf")
