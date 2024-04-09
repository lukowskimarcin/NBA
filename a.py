import networkx as nx
import matplotlib.pyplot as plt

class Node:
    def __init__(self, id: int, action, cost):
        self.id = id
        self.action = action
        self.cost = cost

    def __eq__(self, other):
        if not isinstance(other, Node):
            return False
        return (self.id, self.action, self.cost) == (other.id, other.action, other.cost)

    def __hash__(self):
        return hash((self.id, self.action, self.cost))
    
    def __str__(self) -> str:
        return f"{self.action}"



class Graph:

    def __init__(self) -> None:
        self.graph = nx.DiGraph()
        nodes = [
            Node(0, 'ROOT', 1), #0
            Node(1, 'A', 1),    #1
            Node(2, 'ReZus', 1),    #2
            Node(3, 'C', 1),    #3
            Node(4, 'A', 1),    #4
            Node(5, 'B', 1),    #5
            Node(6, 'C', 1),    #6
            Node(7, 'C', 1)     #7
        ]
        self.graph.add_edge(nodes[0], nodes[1], weight=1)
        self.graph.add_edge(nodes[0], nodes[2], weight=2)
        self.graph.add_edge(nodes[0], nodes[3], weight=3)
        self.graph.add_edge(nodes[1], nodes[4], weight=4)
        self.graph.add_edge(nodes[1], nodes[5], weight=5)
        self.graph.add_edge(nodes[2], nodes[6], weight=6)
        self.graph.add_edge(nodes[2], nodes[7], weight=7)


    def draw(self):
        # https://networkx.org/documentation/stable/auto_examples/graph/plot_dag_layout.html
        for layer, nodes in enumerate(nx.topological_generations(self.graph)):
            # `multipartite_layout` expects the layer as a node attribute, so add the
            # numeric layer value as a node attribute
            for node in nodes:
                self.graph.nodes[node]["layer"] = layer

        # Compute the multipartite_layout using the "layer" node attribute
        pos = nx.multipartite_layout(self.graph, subset_key="layer")


        nx.draw_networkx_nodes(self.graph, pos, node_color="lightblue", node_size=2500)
        nx.draw_networkx_edges(self.graph, pos, edge_color="grey")
        nx.draw_networkx_labels(self.graph, pos, font_size=12, font_family="sans-serif")        
        nx.draw_networkx_edge_labels(
            self.graph, pos, edge_labels={(u, v): d["weight"] for u, v, d in self.graph.edges(data=True)},            
            font_weight="bold"
        )


        nx.draw_networkx_edges(self.graph, pos, edge_color="green", width=1.5, edgelist=[
            (Node(0, 'ROOT', 1), Node(2, 'ReZus', 1)),
            (Node(2, 'ReZus', 1), Node(7, 'C', 1))
        ])
        nx.draw_networkx_nodes(self.graph, pos, node_color="lightgreen", node_size=2700, nodelist=[
            Node(0, 'ROOT', 1), 
            Node(2, 'ReZus', 1),
            Node(7, 'C', 1)
        ])


        plt.axis("off")
        plt.show()



        #fig, ax = plt.subplots()
        #nx.draw_networkx(self.graph, pos=pos, ax=ax , with_labels=True)        
        #fig.tight_layout()
        #plt.show()




g = Graph()      
g.draw()  
