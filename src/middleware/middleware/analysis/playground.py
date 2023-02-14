from middleware.analysis import collocation_graph

graph_generator = collocation_graph.CollocationGraphGenerator("./src/data/", "./src/data/word-graph/")
graph_generator.generate_and_cluster(0, 50000, False, 2, 128, "agglomerative", 12, only_nes=True)
