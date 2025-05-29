import networkx as nx
import random
import matplotlib.pyplot as plt

def create_graph():
    graph = nx.Graph()
    nodes = range(1, 10)
    edges = [(7, 2), (2, 3), (7, 4), (4, 5), (7, 3), (7, 5), (1, 6),
             (1, 7), (2, 8), (2, 9)]
    graph.add_nodes_from(nodes)
    graph.add_edges_from(edges)
    return graph

def visualize_graph(graph):
    pos = nx.spring_layout(graph)
    plt.figure(figsize=(10, 7))
    nx.draw(graph, pos, with_labels=True, node_size=700, node_color='skyblue', font_size=10)
    plt.show()

def calculate_centrality(graph):
    degree_centrality = nx.degree_centrality(graph)
    betweenness_centrality = nx.betweenness_centrality(graph)
    closeness_centrality = nx.closeness_centrality(graph)
    eigenvector_centrality = nx.eigenvector_centrality(graph)

    return degree_centrality, betweenness_centrality, closeness_centrality, eigenvector_centrality

def likelihood(neighbors, T, graph):
    weights = [1 if graph.nodes[i]['role'] == 'F' else 0 for i in neighbors]
    P = sum(weights) / len(neighbors)

    if P >= T:
        print(f"The likelihood is {P}, which means that the person is likely involved in fraud.")
    else:
        print(f"The likelihood is {P}, which means that the person is not involved in fraud.")

def compute_dos(graph, centrality, negative_scores):
    dos_nodes = {}
    for node in graph.nodes:
        centrality_sum = sum([centrality[metric][node] for metric in centrality]) / len(centrality)
        dos_nodes[node] = centrality_sum * negative_scores.get(node, 0)

    max_dos = max(dos_nodes.values())
    normalized_dos = {node: dos / max_dos for node, dos in dos_nodes.items()}
    return normalized_dos

def assign_negative_scores(graph):
    negative_scores = {}
    for node in graph.nodes:
        negative_scores[node] = random.choice([6, 7, 8, 10]) if graph.nodes[node]['role'] == 'F' else 0
    return negative_scores

def main():
    graph = create_graph()

    nx.set_node_attributes(graph, {1: 'NF', 2: 'F', 3: 'NF', 4: 'NF',
                                   5: 'F', 6: 'F', 7: 'F', 8: 'NF', 9: 'NF'}, 'role')

    visualize_graph(graph)

    centrality = {}
    centrality['degree'] = nx.degree_centrality(graph)
    centrality['betweenness'] = nx.betweenness_centrality(graph)
    centrality['closeness'] = nx.closeness_centrality(graph)
    centrality['eigenvector'] = nx.eigenvector_centrality(graph)

    negative_scores = assign_negative_scores(graph)

    normalized_dos = compute_dos(graph, centrality, negative_scores)
    print("Normalized DOS:", normalized_dos)

    likelihood([1, 7, 5], 0.5, graph)

if __name__ == "__main__":
    main()
