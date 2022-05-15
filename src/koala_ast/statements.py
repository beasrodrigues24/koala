from abc import ABC, abstractmethod
from typing import List
import copy
from pretty_print import PrettyPrint
from .variables import Var
from .conditions import Condition


class Statement(ABC):
    @abstractmethod
    def eval(self, dict):
        pass


class Block(Statement):
    def __init__(self, statements: List[Statement]):
        self.statements = statements

    def __repr__(self):
        return f'Block: {repr(self.statements)}'

    def __iter__(self):
        return self.statements.__iter__()

    def eval(self, dict):
        r = ''
        for b in self.statements:
            r += b.eval(dict)

        return r


class Alias(Statement):
    def __init__(self, name: str, vars: List[str], block: Block):
        self.name = name
        self.vars = vars
        self.block = block

    def __repr__(self):
        return f'Alias: {self.name}({self.vars}) {{{self.block}}}'

    def eval(self, dict):
        dict['aliases'][self.name] = self
        return ''


class CallAlias(Statement):
    def __init__(self, alias_name: str, args: List[Var]):
        self.alias_name = alias_name
        self.args = args

    def __repr__(self):
        return f'CallAlias: {self.alias_name}({self.args})'

    def eval(self, dict):
        if self.alias_name not in dict['aliases']:
            PrettyPrint.error(
                f'Alias \'{self.alias_name}\' called but not defined.'
            )
            exit(1)

        alias: Alias = dict['aliases'][self.alias_name]
        if len(self.args) != len(alias.vars):
            PrettyPrint.error(
                f'Wrong number of arguments passed to alias \'{alias.name}\': Expected {len(alias.vars)}, received {len(self.args)}.'
            )
            exit(1)

        new_dict = copy.deepcopy(dict)

        for (var, arg) in zip(alias.vars, self.args):
            new_dict['tmp'][var] = arg.iter(dict)

        r = alias.block.eval(new_dict)

        return r


class For(Statement):
    def __init__(self, tmpvar_name: str, var: Var, block: Block):
        self.tmpvar_name = tmpvar_name
        self.var = var
        self.block = block

    def __repr__(self):
        return f'For: {self.tmpvar_name} : {self.var} {{{self.block}}}'

    def eval(self, dict):
        new_dict = copy.deepcopy(dict)
        r = ''
        if self.var.test(dict):
            for v in self.var.iter(dict):
                new_dict['tmp'][self.tmpvar_name] = v
                r += self.block.eval(new_dict)

        return r


class If():
    def __init__(self, condition: Condition, block: Block):
        self.condition = condition
        self.block = block

    def __repr__(self):
        return f'If: {self.condition} {{{self.block}}}'


class Ifs(Statement):
    def __init__(self, ifs: List[If]):
        self.ifs = ifs

    def __repr__(self):
        return f'Ifs: {repr(self.ifs)}'

    def eval(self, dict):
        for i in self.ifs:
            if i.condition.test(dict):
                return i.block.eval(dict)

        return ''
