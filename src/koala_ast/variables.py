from typing import List
from abc import ABC, abstractmethod
from .conditions import Condition
from .pipes import Pipe
from pretty_print import PrettyPrint

class Iterable(ABC):
    @abstractmethod
    def iter(self, dict):
        pass


class Var(Condition, Iterable):
    def __init__(self, name: List[str], pipes: List[Pipe]):
        self.name = name
        self.pipes = pipes

    def eval(self, dict):
        return str(self.iter(dict))


class DictVar(Var):
    def __repr__(self):
        return f'DictVar: {self.name}'

    def test(self, dict):
        v = dict['variables']
        for x in self.name:
            if x not in v:
                return False
            v = v[x]

        return True

    def iter(self, dict):
        v = dict['variables']
        for x in self.name:
            if x in v:
                v = v[x]
            else:
                PrettyPrint.error(
                    f'Variable \'{".".join(self.name)}\' not found in the dictionary.')
                exit(1)
        for pipe in self.pipes:
            v = pipe.apply(v)
        return v


class TmpVar(Var):
    def __repr__(self):
        return f'TmpVar: {self.name}'

    def test(self, dict):
        tmp = dict['tmp']
        for x in self.name:
            if x not in tmp:
                return False
            tmp = tmp[x]

        return True

    def iter(self, dict):
        v = dict['tmp']
        for x in self.name:
            if x in v:
                v = v[x]
            else:
                PrettyPrint.error(
                    f'Variable \'{".".join(self.name)}\' not in scope.')
                exit(1)
        for pipe in self.pipes:
            v = pipe.apply(v)
        return v


class Text(Var):
    def __init__(self, content: str, pipes: List[Pipe]):
        self.content = content
        self.pipes = pipes

    def __repr__(self):
        return f'Text: \'{self.content}\''.encode('unicode_escape').decode('utf-8')

    def test(self, dict):
        return True

    def iter(self, dict):
        tmp = self.content
        for pipe in self.pipes:
            tmp = pipe.apply(tmp)
        return tmp
