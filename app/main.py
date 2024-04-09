import networkx as nx
import matplotlib.pyplot as plt

class Node:
    def __init__(self, action, cost):
        self.action = action
        self.cost = cost

class Edge:
    def __init__(self, src, dest, weight):
        self.src = src
        self.dest = dest
        self.weight = weight

 

def dfs(graph: nx.Graph, node, visited, path):
    visited.add(node)
    path.append(node)
    max_path = path.copy()  # Zmienna przechowująca aktualnie najlepszą ścieżkę

    for neighbor in graph.neighbors(node):
        if neighbor not in visited:
            new_path = dfs(graph, neighbor, visited, path)
            if sum(edge.weight for edge in new_path) > sum(edge.weight for edge in max_path):
                max_path = new_path

    path.pop()  # Usuwamy wierzchołek z ścieżki
    visited.remove(node)
    return max_path



def draw_graph(graph, path):
    pos = nx.spring_layout(graph)
    nx.draw(graph, pos, with_labels=True, node_color='skyblue', node_size=1500)
    labels = {(edge.src, edge.dest): edge.weight for edge in graph.edges()}
    nx.draw_networkx_edge_labels(graph, pos, edge_labels=labels)
    
    # Rysowanie optymalnej ścieżki
    optimal_edges = [(path[i].action, path[i + 1].action) for i in range(len(path) - 1)]
    nx.draw_networkx_edges(graph, pos, edgelist=optimal_edges, edge_color='r', width=3)

    plt.show()

# Tworzenie grafu
graph = nx.Graph()
nodes = [Node('A', 0), Node('B', 2), Node('C', 3), Node('D', 5), Node('E', 4), Node('F', 6)]
edges = [Edge(nodes[0], nodes[1], 1), Edge(nodes[0], nodes[2], 2), Edge(nodes[1], nodes[3], 3),
         Edge(nodes[1], nodes[4], 4), Edge(nodes[2], nodes[5], 5)]

# Dodawanie wierzchołków i krawędzi do grafu
for node in nodes:
    graph.add_node(node.action)
for edge in edges:
    graph.add_edge(edge.src.action, edge.dest.action, weight=edge.weight)

# Wywołanie DFS
start_node = nodes[0]
visited = set()
optimal_path = dfs(graph, start_node, visited, [])

# Rysowanie grafu wraz z optymalną ścieżką
draw_graph(graph, optimal_path)
