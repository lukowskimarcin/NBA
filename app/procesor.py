from repository import GraphRepository


class GraphsProcessor:

    def __init__(self) -> None:
        self.repository = GraphRepository()

    def process(self):
        for graph in self.repository.find_all():
            graph.build()