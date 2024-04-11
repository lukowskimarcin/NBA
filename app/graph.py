import networkx as nx
from dfs import DFS
from node import Node, NodeState
from graph_chart import GraphChart
from constants import ACTION_MODELS, MAX_COST, MAX_TIME, ROOT_NODE


class NBAGraph:
    """
    Reprezentuje Graf NBA
    """

    def __init__(self, client_id, dlum_id, initial_wps, current_wps) -> None:
        self.client_id = client_id
        self.dlum_id = dlum_id
        self.initial_wps = initial_wps
        self.current_wps = current_wps
        self.is_active = "T" 
        self.best_action_path_nodes: list[Node] = []
        self.next_best_action_name = None
        self.total_cost_spend = 0
        self.total_time_spend = 0

    def show(self):
        """
        Pokazuje aktualny stan grafu NBA
        """
        title = f"""
                 client_id: {self.client_id}, dlum_id: {self.dlum_id}   
                 wps:   ({self.current_wps}/{self.initial_wps})    ({round(100-(100*self.current_wps/self.initial_wps),2)}%)
                 total_cost:    ({self.total_cost_spend}/{MAX_COST})    ({round(100*self.total_cost_spend/MAX_COST,2)}%)
                 total_time:    ({self.total_time_spend}/{MAX_TIME})    ({round(100*self.total_time_spend/MAX_TIME,2)}%)
                 nodes:   {self.graph.number_of_nodes()}
                """
        chart = GraphChart(self.graph, self.nodes, self.best_action_path_nodes, title)
        chart.draw()

    def __calculate_edge_weight(self, pdp):
        return round(self.current_wps * pdp, 4)

    def __generate_layer(self, node: Node, node_sum_cost, node_sum_time):
        """
        Metoda generuje rekurencyjnie kolejne warstwy grafu, do punktu odciecia (koszt + czas)
        """
        for model in ACTION_MODELS:
            cost = model.estimated_cost()
            time = model.estimated_time()

            actual_sum_cost = node_sum_cost + cost
            actual_sum_time = node_sum_time + time

            if (actual_sum_cost <= MAX_COST) and (actual_sum_time <= MAX_TIME):
                # Nie przekroczone koszty mozemy dodac wezel do grafu
                pdp = model.predict(self.client_id, self.dlum_id)
                weight = self.__calculate_edge_weight(pdp)

                self.sequence += 1
                new_node = Node(
                    self.sequence,
                    node.level + 1,
                    model.action_name,
                    NodeState.EMPTY,
                    cost,
                    time,
                )

                self.nodes.append(new_node)
                self.graph.add_edge(node, new_node, weight=weight)

                # rekurencyjne tworzenie kolejnej warstwy
                self.__generate_layer(new_node, actual_sum_cost, actual_sum_time)

    def build(self):
        """
        Metoda generuje inicjalny graf możliwych akcji
        """
        self.graph = nx.DiGraph()
        self.nodes = [ROOT_NODE]
        self.sequence = 0
        self.__generate_layer(ROOT_NODE, 0, 0)

    def __clean_up_from_node(self, node: Node, include: bool = False):
        """
        Usuwa krawedzie i wezly z grafu od wskazanego wezla

        Parametry
        ----------
        node : wezel startowy akcji
        include : czy wskazany wezel rowniez usunac
        """
        if include:
            subgraph_nodes = nx.descendants(self.graph, node) | {node}
        else:
            subgraph_nodes = nx.descendants(self.graph, node)

        self.graph.remove_nodes_from(subgraph_nodes)
        for n in subgraph_nodes:
            self.nodes.remove(n)
            if n in self.best_action_path_nodes:
                self.best_action_path_nodes.remove(n)

    def __find_node_index(self, node):
        """
        Zwraca indeks wezła w self.nodes
        """
        i = 0
        for n in self.nodes:
            if n == node:
                return i
            i += 1
        return -1

    def __get_children_nodes(self, node) -> list[Node]:
        """
        Zwróc liste dzieci wskazanego węzła w grafie
        """
        result = [n for n in self.graph.successors(node)]
        return result

    def __find_best_action_path(self):
        """
        Wyszukuje w grafie aktualna najkorzystniejszą ścieżke działań według sumy wag krawędzi
        """

        dfs_solver = DFS(self.graph)
        visited = set()
        self.best_action_path_nodes = dfs_solver.dfs(self.nodes[0], visited, [])

    def action_performed(
        self, new_current_wps, real_cost=None, real_time=None, recalculate_graph=True
    ):
        """
        Metoda do uruchomienia w momencie wykonania proponowanej akcji NBA i otrzymaniu rezultatow
        W ramch swojego dzialania oczyszcza graf z sciezek, ktore nie sa już możliwe do przejścia
        Dodatkow re-generuje graf od punktu akcji.
        Wyznacza rowniez sume dotychczas poniesionego kosztu i czasu

        Parametry
        ----------
        new_current_wps : aktualny rzeczywisty WPS po wykonaniu akcji
        real_cost : realny koszt wykonania akcji NBA, gdy None nie nadpisuje informacji w wezle
        real_time : realny czas wykonania akcji NBA, gdy None nie nadpisuje informacji w wezle
        recalculate_graph : czy na nowo przeliczyć możliwe opcje akcji od zatwierdzonej
        """

        self.next_best_action_name = None
        self.current_wps = new_current_wps

        if new_current_wps <= 0:
            self.is_active = "N"

        # znajdz aktualny Node i zmien status
        sum_cost = 0
        sum_time = 0

        prev_node = None
        for node in self.best_action_path_nodes:

            if prev_node is not None:
                sum_cost += node.cost
                sum_time += node.time

                if node.state == NodeState.ACTUAL:
                    node.state = NodeState.PERFORMED
                    index = self.__find_node_index(node)
                    self.nodes[index].state = NodeState.PERFORMED
                    if real_cost is not None:
                        sum_cost = sum_cost - node.cost + real_cost
                        node.cost = real_cost

                    if real_time is not None:
                        sum_time = sum_time - node.time + real_time
                        node.time = real_time

                    # usun sciezki ktore staly sie martwe
                    for children in self.__get_children_nodes(prev_node):
                        if children.state == NodeState.EMPTY:
                            self.__clean_up_from_node(children, True)

                    # przegeneruj graf po wykonanej akcji
                    if recalculate_graph:
                        self.__clean_up_from_node(node, False)
                        self.sequence = node.id
                        self.__generate_layer(node, sum_cost, sum_time)
                        self.__find_best_action_path()

                    self.total_cost_spend = sum_cost
                    self.total_time_spend = sum_time

            prev_node = node

    def determine_next_action(self):
        """
        Metoda wyznacza najlepszą następną akcje.
        """
        if self.is_active == "N":
            return None

        self.__find_best_action_path()
        result_node = None

        prev_node = None
        for node in self.best_action_path_nodes:
            if prev_node is not None:
                index = self.__find_node_index(node)

                if (
                    prev_node.state == NodeState.PERFORMED
                    and node.state != NodeState.PERFORMED
                ):
                    self.nodes[index].state = NodeState.ACTUAL
                    node.state = NodeState.ACTUAL
                    result_node = self.nodes[index]

                if node.state == NodeState.EMPTY:
                    self.nodes[index].state = NodeState.FUTURE
                    node.state = NodeState.FUTURE

            prev_node = node

        if result_node is not None:
            self.next_best_action_name = result_node.action
        else:
            self.is_active = "N"

        return result_node

    def __str__(self) -> str:
        return (
            "{"
            + f"""
                client_id: {self.client_id}, 
                dlum_id: {self.dlum_id}, 
                initial_wps: {self.initial_wps}, 
                current_wps: {self.current_wps}, 
                is_active: {self.is_active}
                """
            + "}"
        )
