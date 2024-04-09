import networkx as nx
import matplotlib.pyplot as plt

class Node:
    """
        Reprezentacja wezla i jego stanu
    """

    def __init__(self, id: int, action, cost, time):
        self.id = id

        # Akcja do wykonania
        self.action = action

        # koszty
        self.cost = cost
        self.time = time

    def __eq__(self, other):
        if not isinstance(other, Node):
            return False
        return self.id == other.id

    def __hash__(self):
        return hash((self.id, self.action))
    
    def __str__(self) -> str:
        return f"{self.action}"
    

class Edge:
    def __init__(self, src, dest, weight):
        self.src = src
        self.dest = dest
        self.weight = weight

class Graph:
    def __init__(self):
        self.graph = nx.DiGraph()

    def add_node(self, node):
        self.graph.add_node(node)

    def add_edge(self, edge):
        self.graph.add_edge(edge.src, edge.dest, weight=edge.weight)

    def draw_graph(self, path=None):
        pos = nx.spring_layout(self.graph)
        nx.draw(self.graph, pos, with_labels=True, node_color='skyblue', node_size=1500)
        if path:
            optimal_edges = [(path[i], path[i + 1]) for i in range(len(path) - 1)]
            nx.draw_networkx_edges(self.graph, pos, edgelist=optimal_edges, edge_color='r', width=3)

        # Pobieranie etykiet krawędzi grafu
        labels = {(edge[0], edge[1]): self.graph[edge[0]][edge[1]]['weight'] for edge in self.graph.edges()}
        nx.draw_networkx_edge_labels(self.graph, pos, edge_labels=labels)

        plt.show()

class DFS:
    def __init__(self, graph: nx.DiGraph):
        self.graph = graph

    def __sum_path(self, path):
        weight = 0
        for i in range(1, len(path)):
            weight += self.graph[path[i-1]][path[i]]['weight']
        
        return weight


    def dfs(self, node, visited, path):
        visited.add(node)
        path.append(node)
        max_path = path.copy()  # Zmienna przechowująca aktualnie najlepszą ścieżkę

        for neighbor in self.graph.neighbors(node):
            if neighbor not in visited:
                new_path = self.dfs(neighbor, visited, path)

                if self.__sum_path(new_path) > self.__sum_path(max_path):
                    max_path = new_path


        path.pop()  # Usuwamy wierzchołek z ścieżki
        visited.remove(node)
        return max_path

# Użycie klas
graph = Graph()
#nodes = [Node('A', 0), Node('B', 2), Node('C', 3), Node('D', 5), Node('E', 4), Node('F', 6)]
#edges = [Edge(nodes[0], nodes[1], 1), Edge(nodes[0], nodes[2], 2), Edge(nodes[1], nodes[3], 3),   Edge(nodes[1], nodes[4], 4), Edge(nodes[2], nodes[5], 5)]


nodes = [
    Node(0,'ROOT', 0, 0),    #0
    
    Node(1,'A1', 1, 1),       #1
    Node(2,'B1', 1, 1),       #2
    Node(3,'C1', 1, 1),       #3

    Node(4,'A2', 1, 1),       #4
    Node(5,'B2', 1, 1),       #5
    Node(6,'C2', 1, 1),       #6

    Node(7,'A3', 1, 1),       #7
    Node(8,'B3', 1, 1),       #8
    Node(9,'C3', 1, 1),       #9

    Node(10,'A4', 1, 1),       #10
    Node(11,'B4', 1, 1),       #11    
    Node(12,'C4', 1, 1)       #12    
]    

edges = [
    Edge(nodes[0], nodes[1], 10),
    Edge(nodes[0], nodes[2], 3),
    Edge(nodes[0], nodes[3], 7),

    Edge(nodes[1], nodes[4], 10),
    Edge(nodes[1], nodes[5], 10),
    Edge(nodes[1], nodes[6], 10),

    Edge(nodes[2], nodes[7], 10),
    Edge(nodes[2], nodes[8], 10),
    Edge(nodes[2], nodes[9], 10),

    Edge(nodes[3], nodes[10], 10),
    Edge(nodes[3], nodes[11], 10),

    Edge(nodes[5], nodes[12], 10)
]



for node in nodes:
    graph.add_node(node)
for edge in edges:
    graph.add_edge(edge)

dfs_solver = DFS(graph.graph)
start_node = nodes[0]
visited = set()
optimal_path = dfs_solver.dfs(start_node, visited, [])

graph.draw_graph()
