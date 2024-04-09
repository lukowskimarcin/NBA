import networkx as nx
import matplotlib.pyplot as plt
from actions import ActionModel
from node import Node, ROOT_NODE, NodeState


MAX_COST = 200  # Maksymalny koszt
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
    ) -> None:
        self.client_id = client_id
        self.dlum_id = dlum_id
        self.initial_wps = initial_wps
        self.current_wps = current_wps
        self.best_action_path = best_action_path
        self.is_action_performed = is_action_performed

        self.best_action_path_nodes = [
            ROOT_NODE,
            Node(1, "A", NodeState.ACTUAL, 1, 1),
            Node(2, "B", NodeState.FUTURE, 1, 1),
        ]

    def __str__(self) -> str:
        return (
            "{"
            + f"""client_id: {self.client_id}, 
                dlum_id: {self.dlum_id}, 
                initial_wps: {self.initial_wps}, 
                current_wps: {self.current_wps}, 
                best_action_path: {self.best_action_path},
                is_action_performed: {self.is_action_performed}
                """
            + "}"
        )

    def build(self, models: list[ActionModel]):
        """
        buduje graf na podstawie aktualnych danych
        """

        pass

    def draw(self):
        pass
