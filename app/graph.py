import networkx as nx
import matplotlib.pyplot as plt
from actions import ActionModel, ACTION_MODELS
from node import Node, ROOT_NODE, NodeState
import json

MAX_COST = 40  # Maksymalny koszt
MAX_TIME = 18  # Maksymalny czas zycia sprawy


class NBAGraph:
    """
    Reprezentuje Graf NBA
    """

    def __init__(
        self,
        client_id,
        dlum_id,
        initial_wps,
        current_wps,
        best_action_path,
        is_action_performed,
        is_active,
    ) -> None:
        self.client_id = client_id
        self.dlum_id = dlum_id
        self.initial_wps = initial_wps
        self.current_wps = current_wps
        self.best_action_path = best_action_path
        self.is_action_performed = is_action_performed
        self.is_active = is_active

        # obiekty Node
        self.best_action_path_nodes: list[Node] = []
        if self.best_action_path is not None and len(self.best_action_path) > 0:
            for data in json.loads(self.best_action_path):
                node = Node.from_dict(data)

                if self.is_action_performed and node.state == NodeState.ACTUAL:
                    node.state = NodeState.PERFORMED
                self.best_action_path_nodes.append(node)

        print(f"END init")

    def __generate_layer(
        self, node: Node, models: list[ActionModel], node_sum_cost, node_sum_time
    ):
        visited_layer = False
        last_best_node = None

        if len(self.best_action_path_nodes) - 1 >= node.level + 1:
            last_best_node = self.best_action_path_nodes[node.level + 1]

            if last_best_node.state == NodeState.PERFORMED:
                visited_layer = True

        for model in models:
            # przycinanie zbendnych rozgalezien w grafie
            if (
                visited_layer
                and last_best_node is not None
                and last_best_node.action == model.action_name
            ) or not visited_layer:
                cost = model.cost()
                time = model.time()

                actual_sum_cost = node_sum_cost + cost
                actual_sum_time = node_sum_time + time

                if (actual_sum_cost < MAX_COST) and (actual_sum_time < MAX_TIME):
                    # Nie przekroczone koszty mozemy dodac wezel do grafu
                    pdp = model.predict(self.client_id, self.dlum_id)
                    weight = self.current_wps * pdp

                    if (
                        visited_layer
                        and last_best_node is not None
                        and last_best_node.action == model.action_name
                    ):
                        new_node = Node(
                            node.level + 1,
                            model.action_name,
                            NodeState.PERFORMED,
                            cost,
                            time,
                        )
                        self.best_action_path_nodes[node.level + 1] = new_node
                    else:
                        new_node = Node(
                            node.level + 1,
                            model.action_name,
                            NodeState.EMPTY,
                            cost,
                            time,
                        )

                    self.nodes.append(new_node)
                    self.graph.add_edge(node, new_node, weight=weight)

                    # rekurencyjne tworzenie kolejnej warstwy
                    self.__generate_layer(
                        new_node, models, actual_sum_cost, actual_sum_time
                    )
                else:
                    print(f"{node.level}-{node.action} -> END PATH")

    def build(self, models: list[ActionModel]):
        self.graph = nx.DiGraph()
        self.nodes = [ROOT_NODE]

        self.__generate_layer(ROOT_NODE, models, 0, 0)
        print(f"End build Graph")

    def calculate_next_action(self):
        # wyznacz nastepna akcje do wykonania na dlugu
        pass

    def draw(self):
        # https://networkx.org/documentation/stable/auto_examples/graph/plot_dag_layout.html
        for layer, nodes in enumerate(nx.topological_generations(self.graph)):
            # `multipartite_layout` expects the layer as a node attribute, so add the
            # numeric layer value as a node attribute
            for node in nodes:
                self.graph.nodes[node]["layer"] = layer

        # Compute the multipartite_layout using the "layer" node attribute
        pos = nx.multipartite_layout(self.graph, subset_key="layer")

        nx.draw_networkx_nodes(self.graph, pos, node_color="lightblue", node_size=2000)
        nx.draw_networkx_edges(self.graph, pos, edge_color="grey")
        nx.draw_networkx_labels(self.graph, pos, font_size=8, font_family="sans-serif")
        nx.draw_networkx_edge_labels(
            self.graph,
            pos,
            edge_labels={
                (u, v): d["weight"] for u, v, d in self.graph.edges(data=True)
            },
            font_weight="bold",
        )

        plt.axis("off")
        plt.show()

    def __str__(self) -> str:
        return (
            "{"
            + f"""
                client_id: {self.client_id}, 
                dlum_id: {self.dlum_id}, 
                initial_wps: {self.initial_wps}, 
                current_wps: {self.current_wps}, 
                best_action_path: {self.best_action_path},
                is_action_performed: {self.is_action_performed},
                is_active: {self.is_active}
                """
            + "}"
        )


if __name__ == "__main__":
    graph = NBAGraph(1, 1, 1000, 1000, None, "N", "T")
    graph.build(ACTION_MODELS)

    print(f"graph: {graph}")
    graph.draw()
#    graph.draw()
