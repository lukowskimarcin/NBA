from actions import ACTION_MODELS
from repository import GraphRepository


class GraphsProcessor:

    def __init__(self) -> None:
        self.repository = GraphRepository()

    def process(self):
        # for graph in self.repository.find_all():

        graph = self.repository.findById(1, 1)

        # buduj graf
        graph.build(ACTION_MODELS)

        # pokaza jak wyglada graf
        graph.show()

        # wyznacz
        graph.determine_next_action()

        # pokaz jak wyglada graf po wyznaczeniu akcji
        graph.show()

        self.repository.save(graph)


if __name__ == "__main__":
    procesor = GraphsProcessor()
    procesor.process()
