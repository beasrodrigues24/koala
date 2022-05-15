from abc import ABC, abstractmethod

class Pipe(ABC):
    @abstractmethod
    def apply(self, it):
        pass


class PipeFirst(Pipe):
    def apply(self, it):
        return it[0]


class PipeLast(Pipe):
    def apply(self, it):
        return it[-1]


class PipeHead(Pipe):
    def apply(self, it):
        return it[:-1]


class PipeTail(Pipe):
    def apply(self, it):
        return it[1:]
