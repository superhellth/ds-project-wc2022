from collections import defaultdict
import ast
import numpy as np
import networkx as nx
import spacy
from node2vec import Node2Vec
from sklearn.cluster import KMeans
from sklearn.cluster import AgglomerativeClustering
from sklearn.cluster import SpectralClustering
from sklearn.cluster import MeanShift
from sklearn.cluster import AffinityPropagation
from sklearn.cluster import DBSCAN
from sklearn.cluster import OPTICS
from sklearn.cluster import Birch
from sklearn.cluster import MiniBatchKMeans
from sklearn.preprocessing import LabelEncoder
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
            print("Reading unclustered graph from file...")
            G = nx.read_gexf(self.path_to_graph_files + unclusterd_graph_file)
        except (FileNotFoundError, OSError):
            print("Graph file does not exists yet. Generating it...")
            G = self.generate_graph(window_size=window_size, num_edges=num_edges, include_stop_word_nodes=include_stop_word_nodes, min_node_length=min_node_length)
            nx.write_gexf(G, self.path_to_graph_files + unclusterd_graph_file)
        return G

    def color_edges(self, graph: nx.Graph):
        """Color edges between nodes of the same color with the according color."""
        for (u, v) in graph.edges():
            if graph.nodes[u]["color"] == graph.nodes[v]["color"]:
                graph.edges[(u, v)]["color"] = graph.nodes[v]["color"]
        return graph

    def color_nodes(self, graph: nx.Graph, n_cluster: int, node_to_cluster: dict):
        """Color nodes according to cluster."""
        for i in range(n_cluster):
            cluster_color = self.colors[i % len(self.colors)]
            cluster_nodes = [node for node in graph.nodes if node in node_to_cluster.keys() and node_to_cluster[node] == i]
            for node in cluster_nodes:
                graph.nodes[node]["color"] = cluster_color
        return graph

    def learn_node2vec(self, graph: nx.Graph, embedding_size):
        """Generate a node2vec embedding for the given graph."""
        node2vec = Node2Vec(graph, dimensions=embedding_size, workers=4)
        print("Learning embedding...")
        return node2vec.fit(window=10, min_count=1)

    def get_embedding(self, graph, window_size, num_edges, embedding_size):
        """Read embedding file. If not exists: generate embedding."""
        embedding_file = "embedding_" + "windowsize=" + str(window_size) + "-edges=" + str(num_edges) + "_embeddingsize=" + str(embedding_size) + ".emb"
        try:
            print("Reading embedding from file...")
            return np.loadtxt(self.path_to_graph_files + embedding_file, skiprows=1, dtype=str, encoding="utf_8", delimiter=" ", comments=None)
        except (FileNotFoundError, OSError):
            print("Embedding file does not exists yet. Generating it...")
            emb = self.learn_node2vec(graph, embedding_size)
            emb.wv.save_word2vec_format(self.path_to_graph_files + embedding_file)
        return np.loadtxt(self.path_to_graph_files + embedding_file, skiprows=1, dtype=str, encoding="utf_8", delimiter=" ", comments=None)
        
    def cluster(self, graph: nx.Graph, n_clusters, algorithm: str, embedding: np.array=None):
        """Cluster the given graph using the given clusterer."""
        print("Clustering...")
        algorithms = ["spectral", "k-means", "agglomerative", "mean-shift", "affinity-propagation", "dbscan", "optics", "birch", "mini-batch-k-means"]
        if algorithm not in algorithms:
            print("Algorithm unknown. Should be one of:")
            print(algorithms)
            return graph

        if embedding is not None:
            X = embedding
            X = X[X[:,0].argsort()]
            Z = X[0:X.shape[0],1:X.shape[1]]
            Z = Z.astype(np.float64)
        else:
            le = LabelEncoder()
            Z = le.fit_transform(graph.nodes()).reshape(-1, 1)

        if algorithm == "k-means":
            clusterer = KMeans(n_clusters=n_clusters)
        elif algorithm == "agglomerative":
            clusterer = AgglomerativeClustering(n_clusters=n_clusters)
        elif algorithm == "spectral":
            clusterer = SpectralClustering(n_clusters=n_clusters)
        elif algorithm == "mean-shift":
            clusterer = MeanShift()
        elif algorithm == "affinity-propagation":
            clusterer = AffinityPropagation()
        elif algorithm == "dbscan":
            clusterer = DBSCAN()
        elif algorithm == "optics":
            clusterer = OPTICS()
        elif algorithm == "birch":
            clusterer = Birch(n_clusters=n_clusters)
        elif algorithm == "mini-batch-k-means":
            clusterer = MiniBatchKMeans(n_clusters=n_clusters)
        res = clusterer.fit(Z)
        node_clusters = res.labels_
        if embedding is not None:
            node_to_cluster = dict(zip(X[:,0], node_clusters))
        else:
            original_labels = le.inverse_transform(node_clusters)
            node_to_cluster = dict(zip(original_labels, node_clusters))
        return self.color_nodes(graph, n_clusters, node_to_cluster)

    def generate_and_cluster(self, window_size, num_edges, include_stop_word_nodes, min_node_length, embedding_size, cluster_alg, n_clusters=-1, color_edges=False):
        """Generates and clusters graph with the given parameters. Saves to file. -1 embedding size to not use embedding."""
        graph_file = "c_ws=" + str(window_size) + "_edges=" + str(num_edges) + "_includestop=" + str(include_stop_word_nodes) + "_minnodelength=" + str(min_node_length) + "_embeddingsize=" + str(embedding_size) + "_clusteralg=" + cluster_alg + "_nclusters=" + str(n_clusters) + "_colorededges=" + str(color_edges) + ".gexf"
        try:
            print("Reading clustered graph from file...")
            graph = nx.read_gexf(self.path_to_graph_files + graph_file)
        except (FileNotFoundError, OSError):
            print("Graph file does not exists yet. Generating it...")
            graph = self.get_graph(window_size=window_size, num_edges=num_edges, include_stop_word_nodes=include_stop_word_nodes, min_node_length=min_node_length)
            if embedding_size == -1:
                embedding = None
            else:
                embedding = self.get_embedding(graph, window_size, num_edges, embedding_size)
            graph = self.cluster(graph, n_clusters, cluster_alg, embedding)
            if color_edges:
                graph = self.color_edges(graph)
            nx.write_gexf(graph, self.path_to_graph_files + graph_file)
        return graph_file

graph_gen = CollocationGraphGenerator("./src/data/", "./src/data/word-graph/")