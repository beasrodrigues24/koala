from typing import List
from abc import ABC, abstractmethod
from .conditions import Condition
from pretty_print import PrettyPrint


class Iterable(ABC):
    @abstractmethod
    def iter(self, dict):
        pass


class Var(Condition, Iterable):
    def __init__(self, name: str):
        self.name = name

    def eval(self, dict):
        return str(self.iter(dict))


class DictVar(Var):
    def __repr__(self):
        return f'DictVar: {self.name}'

    def test(self, dict):
        return dict['variables'].get(self.name) != None

    def iter(self, dict):
        v = dict['variables'].get(self.name)
        if v:
            return v
        else:
            panic(
                f'Variable \'{".".join(self.name)}\' not found in the dictionary.')


class TmpVar(Var):
    def __repr__(self):
        return f'TmpVar: {self.name}'

    def test(self, dict):
        return self.name in dict['tmp'].get(self.name) != None

    def iter(self, dict):
        v = dict['tmp'].get(self.name)
        if v:
            return v
        else:
            panic(f'Temporary variable \'{self.name}\' not in scope.')


class Text(Var):
    def __init__(self, content: str):
        self.content = content

    def __repr__(self):
        return f'Text: \'{self.content}\''.encode('unicode_escape').decode('utf-8')

    def test(self, dict):
        return True

    def iter(self, dict):
        return self.content


class Field(Var):
    def __init__(self, var: Var, field_name: str):
        self.name = f"{var.name}.{field_name}"
        self.var = var
        self.field_name = field_name

    def __repr__(self):
        return f'Field: {self.name}'

    def test(self, dict):
        return self.var.iter(dict).get(self.field_name) != None

    def iter(self, dict):
        v = self.var.iter(dict).get(self.field_name)
        if v:
            return v
        else:
            panic(f'Variable \'{self.name}\' not in scope.')


class Pipe(Var):
    pipes = {
        'first': lambda l: l[0],
        'last': lambda l: l[-1],
        'head': lambda l: l[:-1],
        'tail': lambda l: l[1:],
        'upper': lambda s: s.upper(),
        'lower': lambda s: s.lower(),
        'reverse': lambda l: l[::-1],
    }

    def __init__(self, var: Var, pipe: str):
        self.name = f"{var.name}/{pipe}"
        self.var = var
        p = self.pipes.get(pipe)
        if p:
            self.pipe = p
        else:
            panic(f'Usage of unknown pipe: {pipe}')

    def __repr__(self):
        return f'Pipe: {self.name}'

    def test(self, dict):
        try:
            self.pipe(self.var.eval(dict))
            return True
        except Exception:
            return False

    def iter(self, dict):
        try:
            return self.pipe(self.var.iter(dict))
        except Exception:
            panic(f'Cannot process pipe: {self.name}')


def panic(msg: str):
    PrettyPrint.error(msg)
    exit(1)
