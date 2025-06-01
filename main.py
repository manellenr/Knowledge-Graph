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

    roles = {1: 'NF', 2: 'F', 3: 'NF', 4: 'NF',
             5: 'F', 6: 'F', 7: 'F', 8: 'NF', 9: 'NF'}
    nx.set_node_attributes(graph, roles, 'role')

    return graph

def visualize_graph(graph):
    color = []
    label = {}
    for node in graph.nodes():
        role = graph.nodes[node]['role']
        label[node] = f"{node} ({role})"
        color.append('red' if role == 'F' else 'green')

    pos = nx.spring_layout(graph)
    plt.figure(figsize=(10, 7))
    nx.draw(graph, pos, with_labels=True, labels=label,
            node_color=color, node_size=700, font_size=10)
    plt.title("Graph with Fraud (F) and Non-Fraud (NF) Roles")
    plt.show()

def calculate_centrality(graph):
    degree = nx.degree_centrality(graph)
    betweenness = nx.betweenness_centrality(graph)
    closeness = nx.closeness_centrality(graph)
    eigenvector = nx.eigenvector_centrality(graph)

    print("\nDegree Centrality:", degree)
    print("Betweenness Centrality:", betweenness)
    print("Closeness Centrality:", closeness)
    print("Eigenvector Centrality:", eigenvector)

    return {
        'degree': degree,
        'betweenness': betweenness,
        'closeness': closeness,
        'eigenvector': eigenvector
    }

def likelihood(neighbors, T, graph):
    weights = [1 if graph.nodes[i]['role'] == 'F' else 0 for i in neighbors]
    P = sum(weights) / len(neighbors)

    if P >= T:
        print(f"\nLikelihood: {P:.2f} — Person is LIKELY involved in fraud.")
    else:
        print(f"\nLikelihood: {P:.2f} — Person is NOT likely involved in fraud.")

def assign_negative_scores(graph):
    negative_scores = {}
    for node in graph.nodes:
        negative_scores[node] = random.choice([6, 7, 8, 10]) if graph.nodes[node]['role'] == 'F' else 0
    print("\nAssigned negative scores (fraud nodes):", negative_scores)
    return negative_scores

def compute_dos(graph, centrality, negative_scores):
    dos_nodes = {}
    for node in graph.nodes:
        centrality_avg = sum([centrality[metric][node] for metric in centrality]) / len(centrality)
        dos_nodes[node] = centrality_avg * negative_scores.get(node, 0)

    max_dos = max(dos_nodes.values()) if dos_nodes else 1
    normalized_dos = {node: val / max_dos for node, val in dos_nodes.items()}
    print("\nNormalized Degree of Suspicion (DoS):", normalized_dos)
    return normalized_dos

def main():
    graph = create_graph()
    visualize_graph(graph)

    centrality = calculate_centrality(graph)
    negative_scores = assign_negative_scores(graph)

    normalized_dos = compute_dos(graph, centrality, negative_scores)

    likelihood([1, 7, 5], T=0.5, graph=graph)

if __name__ == "__main__":
    main()
