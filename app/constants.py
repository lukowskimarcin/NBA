from actions import EKW, PassAction, ReOgnivo, ReZus, Teren, ActionModel
from node import NodeState, Node


MAX_COST = 12  # Maksymalny koszt
MAX_TIME = 18  # Maksymalny czas zycia sprawy

ROOT_NODE = Node(0, 0, "ROOT", NodeState.PERFORMED, 0, 0)

ACTION_MODELS: list[ActionModel] = [
    ReZus(),
    ReOgnivo(),
    Teren(),
    EKW(),
    # PassAction(),
]
