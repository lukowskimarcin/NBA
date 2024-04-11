from abc import ABC, abstractmethod
import random


class ActionModel(ABC):
    def __init__(self, action_name) -> None:
        self.action_name = action_name

    @abstractmethod
    def predict(self, client_id, dlum_id):
        pass

    @abstractmethod
    def estimated_cost(self):
        pass

    @abstractmethod
    def estimated_time(self):
        pass

    def __str__(self) -> str:
        return f"Model for Action: {self.action_name}"


class ReZus(ActionModel):
    def __init__(self) -> None:
        super().__init__("ReZus")

    def predict(self, client_id, dlum_id):
        return round(random.random(), 4)

    def estimated_cost(self):
        return random.randint(1, 6)

    def estimated_time(self):
        return random.randint(1, 3)


class ReOgnivo(ActionModel):
    def __init__(self) -> None:
        super().__init__("ReOgnivo")

    def predict(self, client_id, dlum_id):
        return round(random.random(), 4)

    def estimated_cost(self):
        return random.randint(1, 10)

    def estimated_time(self):
        return random.randint(2, 3)


class Teren(ActionModel):
    def __init__(self) -> None:
        super().__init__("Teren")

    def predict(self, client_id, dlum_id):
        return round(random.random(), 4)

    def estimated_cost(self):
        return random.randint(2, 7)

    def estimated_time(self):
        return random.randint(1, 3)


class EKW(ActionModel):
    def __init__(self) -> None:
        super().__init__("EKW")

    def predict(self, client_id, dlum_id):
        return round(random.random(), 4)

    def estimated_cost(self):
        return random.randint(1, 5)

    def estimated_time(self):
        return random.randint(1, 3)


class PassAction(ActionModel):
    def __init__(self) -> None:
        super().__init__("PASS")

    def predict(self, client_id, dlum_id):
        return round(random.random(), 4)

    def estimated_cost(self):
        return 2

    def estimated_time(self):
        return 1
