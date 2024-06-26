from enum import Enum
import json


class NodeState(Enum):
    EMPTY = 0
    PERFORMED = 1
    ACTUAL = 2
    FUTURE = 3

    def iterate_enum_members():
        for state in NodeState.__members__.values():
            yield state


class Node:
    """
    Reprezentacja wezla i jego stanu
    """

    def __init__(self, id: int, level: int, action: str, state: NodeState, cost, time):
        self.id = id
        self.level = level
        self.action = action
        self.state = state
        self.cost = cost
        self.time = time

    def __eq__(self, other):
        if not isinstance(other, Node):
            return False
        return (self.id, self.level, self.action) == (
            other.id,
            other.level,
            other.action,
        )

    def __hash__(self):
        return hash((self.id, self.level, self.action))

    def __str__(self) -> str:
        return f"{self.action}\nc:{self.cost}\nt:{self.time}"

    def to_dict(self):
        return {
            "id": self.id,
            "level": self.level,
            "action": self.action,
            "state": self.state.name,
            "cost": self.cost,
            "time": self.time,
        }

    @classmethod
    def from_dict(cls, data):
        return cls(
            data["id"],
            data["level"],
            data["action"],
            NodeState[data["state"]],
            data["cost"],
            data["time"],
        )


if __name__ == "__main__":
    node = Node(0, 1, "example", NodeState.PERFORMED, 10, 20)
    node_dict = node.to_dict()
    print("Node as dictionary:", node_dict)

    node_json = json.dumps(node_dict)
    print("Node as JSON:", node_json)

    converted_node_dict = json.loads(node_json)
    converted_node = Node.from_dict(converted_node_dict)
    print("Converted Node from JSON:", converted_node)
