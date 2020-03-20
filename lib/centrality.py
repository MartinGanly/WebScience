from lib import interactiongraph
import plotly.graph_objects as go
import networkx as nx
import matplotlib.pyplot as plt
import operator
from itertools import combinations

# Calculates multiple centrality measures
class centrality():

    def in_out_centrality(self, data):
        if len(data) == 0:
            return None, None
        in_degree = {}
        out_degree = {}
        for user, connects in data.items():
            for connect in connects:
                if not user in out_degree:
                    out_degree[user] = 1
                else:
                    out_degree[user] = out_degree[user] + 1
                if not connect in in_degree:
                    in_degree[connect] = 1
                else:
                    in_degree[connect] = in_degree[connect] + 1
        return in_degree, out_degree

    def betweenness(self, data):
        graph = self.create_network(data)
        print("GRAPH CREATED")
        centrality = nx.betweenness_centrality(graph)
        return centrality

    def closeness(self, data):
        graph = self.create_network(data)
        centrality = nx.closeness_centrality(graph)
        return centrality

    def eigenvector(self, data):
        graph = self.create_network(data)
        if graph:
            centrality = nx.eigenvector_centrality(graph, max_iter=50000)
            return centrality
        return None

    def triads(self, data):
        graph = self.create_network(data)

        triad_class = [[],[],[],[]]

        i = 0
        for nodes in combinations(graph.subgraph(data).nodes, 3):
            print("WORKING ON NODE " + str(i) + "/" + str(len(nodes)))
            n_edges = graph.subgraph(nodes).number_of_edges()
            triad_class[n_edges].append(nodes)
            i = i + 1

    def process_network(self, data):
        edges = []
        nodes = []

        for user, connects in data.items():
            nodes.append(user)
            for connect in connects:
                edges.append((user, connect))

        return nodes, edges

    def create_network(self, data):
        graph = nx.Graph()
        for user, connects in data.items():
            graph.add_node(user)
            for connect in connects:
                edge = (user, connect)
                graph.add_edge(*edge)
        return graph

    def visualise(self, graph):
        nx.draw(graph)
        plt.show()
