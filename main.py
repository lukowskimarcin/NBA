from abc import ABC, abstractmethod
import networkx as nx
import matplotlib.pyplot as plt
import random

#===============================================================================================================
class Node:
    """
        Reprezentacja wezla i jego stanu
    """

    def __init__(self, id: int, action, cost, time):
        self.id = id

        # Akcja do wykonania
        self.action = action

        # koszty
        self.cost = cost
        self.time = time

    def __eq__(self, other):
        if not isinstance(other, Node):
            return False
        return self.id == other.id

    def __hash__(self):
        return hash((self.id, self.action))
    
    def __str__(self) -> str:
        return f"{self.action}"

#===============================================================================================================
class ActionModel(ABC):
    def __init__(self, action_name) -> None:
        self.action_name = action_name

    @abstractmethod
    def predict(self, client_id, nk_dum_id):
        pass
    
    @abstractmethod
    def cost(self):
        pass

    def __str__(self) -> str:
        return f"Model for Action: {self.action_name}"


class ReZus(ActionModel):
    def __init__(self) -> None:
        super().__init__('ReZus')

    def predict(self, client_id, nk_dum_id):                
        return round(random.random(), 4)
    
    def cost(self):
        return random.randint(1, 10)
    
class ReOgnivo(ActionModel):
    def __init__(self) -> None:
        super().__init__('ReOgnivo')

    def predict(self, client_id, nk_dum_id):                
        return round(random.random(), 4)
    
    def cost(self):
        return random.randint(1, 10)    
    
class PassAction(ActionModel):
    def __init__(self) -> None:
        super().__init__('PASS')

    def predict(self, client_id, nk_dum_id):                
        return round(random.random(), 4)
    
    def cost(self):
        return 1  




ACTION_MODELS = [
    ReZus(),
    ReOgnivo(),    
    PassAction(),
]

#===============================================================================================================

MAX_COST = 200      # Maksymalny koszt
MAX_TIME = 18       # Maksymalny czas zycia sprawy

class NBAGraph:    
    """
        Reprezentuje Graf NBA
    """

    def __init__(self, 
                 client_id, 
                 nk_dum_id, 
                 initial_wps, 
                 current_wps
                ) -> None:
        pass


    def build(self):
        """
            buduje graf na podstawie aktualnych danych
        """

        pass




#===============================================================================================================
class GraphRepository:

    def find_all() -> list[NBAGraph]:
        return []


    def save(graph: NBAGraph):
        pass

    def load(client_id, nk_dum_id) -> NBAGraph:
        """
            Wczytuje dla zadanego klienta i dluga dane z bazy i 
            tworzy obiekt grafu
        """

        graph =  NBAGraph(client_id, nk_dum_id)
        return graph



#===============================================================================================================
class GraphsProcessor:

    def __init__(self) -> None:
        self.repository = GraphRepository()

    def process(self):
        for graph in self.repository.find_all():
            graph.build()

