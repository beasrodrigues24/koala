from abc import ABC, abstractmethod


class Condition(ABC):
    @abstractmethod
    def test(self, dict):
        pass


class Bool(Condition):
    def __init__(self, bool: bool):
        self.bool = bool

    def test(self, dict):
        return bool
