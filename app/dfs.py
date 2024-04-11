import networkx as nx
from node import Node


class DFS:
    def __init__(self, graph: nx.DiGraph):
        self.graph = graph

    def __sum_path(self, path):
        weight = 0
        for i in range(1, len(path)):
            weight += self.graph[path[i - 1]][path[i]]["weight"]

        return weight

    def dfs(self, node, visited, path) -> list[Node]:
        visited.add(node)
        path.append(node)
        max_path = path.copy()

        for neighbor in self.graph.neighbors(node):
            if neighbor not in visited:
                new_path = self.dfs(neighbor, visited, path)

                if self.__sum_path(new_path) > self.__sum_path(max_path):
                    max_path = new_path

        path.pop()
        visited.remove(node)
        return max_path
