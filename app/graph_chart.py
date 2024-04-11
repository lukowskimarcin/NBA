import networkx as nx
from node import Node, NodeState
import matplotlib.pyplot as plt


plt.rcParams["figure.figsize"] = (22, 12)


class GraphChart:

    def __init__(
        self, graph: nx.DiGraph, nodes: list[Node], path: list[Node], title: str
    ) -> None:
        self.graph = graph
        self.nodes = nodes
        self.title = title
        self.path = path

    def __create_path_edge_list(self):
        if len(self.path) < 2:
            return []
        else:
            result = []
            for i in range(len(self.path) - 1):
                if self.path[i + 1].state != NodeState.EMPTY:
                    result.append((self.path[i], self.path[i + 1]))

            return result

    def draw(self):
        # https://networkx.org/documentation/stable/auto_examples/graph/plot_dag_layout.html
        for layer, nodes in enumerate(nx.topological_generations(self.graph)):
            # `multipartite_layout` expects the layer as a node attribute, so add the
            # numeric layer value as a node attribute
            for node in nodes:
                self.graph.nodes[node]["layer"] = layer

        # Compute the multipartite_layout using the "layer" node attribute
        pos = nx.multipartite_layout(self.graph, subset_key="layer")

        # kolorowanie stanow:
        NODE_COLORS = ["lightblue", "#6eaa5e", "pink", "#dbead5"]
        for state in NodeState.iterate_enum_members():
            nodelist = []
            for node in self.nodes:
                if node.state == state:
                    nodelist.append(node)

            nx.draw_networkx_nodes(
                self.graph,
                pos,
                node_color=NODE_COLORS[state.value],
                node_size=3000,
                nodelist=nodelist,
            )

        nx.draw_networkx_edges(self.graph, pos, edge_color="grey")
        nx.draw_networkx_edges(
            self.graph,
            pos,
            edge_color="#6eaa5e",
            width=1.5,
            edgelist=self.__create_path_edge_list(),
        )
        nx.draw_networkx_labels(self.graph, pos, font_size=6, font_family="sans-serif")
        nx.draw_networkx_edge_labels(
            self.graph,
            pos,
            edge_labels={
                (u, v): d["weight"] for u, v, d in self.graph.edges(data=True)
            },
        )

        plt.axis("off")
        plt.title(
            self.title,
            loc="left",
        )
        plt.show()
