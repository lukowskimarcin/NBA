from abc import ABC, abstractmethod
import random


class ActionModel(ABC):
    def __init__(self, action_name) -> None:
        self.action_name = action_name

    @abstractmethod
    def predict(self, client_id, dlum_id):
        pass

    @abstractmethod
    def cost(self):
        pass

    @abstractmethod
    def time(self):
        pass

    def __str__(self) -> str:
        return f"Model for Action: {self.action_name}"


class ReZus(ActionModel):
    def __init__(self) -> None:
        super().__init__("ReZus")

    def predict(self, client_id, dlum_id):
        return round(random.random(), 4)

    def cost(self):
        return random.randint(1, 10)

    def time(self):
        return random.randint(1, 4)


class ReOgnivo(ActionModel):
    def __init__(self) -> None:
        super().__init__("ReOgnivo")

    def predict(self, client_id, dlum_id):
        return round(random.random(), 4)

    def cost(self):
        return random.randint(1, 10)

    def time(self):
        return random.randint(2, 4)


class Teren(ActionModel):
    def __init__(self) -> None:
        super().__init__("Teren")

    def predict(self, client_id, dlum_id):
        return round(random.random(), 4)

    def cost(self):
        return random.randint(1, 10)

    def time(self):
        return random.randint(1, 4)


class EKW(ActionModel):
    def __init__(self) -> None:
        super().__init__("EKW")

    def predict(self, client_id, dlum_id):
        return round(random.random(), 4)

    def cost(self):
        return random.randint(1, 10)

    def time(self):
        return random.randint(1, 4)


class PassAction(ActionModel):
    def __init__(self) -> None:
        super().__init__("PASS")

    def predict(self, client_id, dlum_id):
        return round(random.random(), 4)

    def cost(self):
        return 1

    def time(self):
        return 1


ACTION_MODELS = [
    ReZus(),
    ReOgnivo(),
    Teren(),
    EKW(),
    PassAction(),
]
