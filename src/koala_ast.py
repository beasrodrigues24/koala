from abc import ABC, abstractmethod
from typing import List
import copy


class Statement(ABC):
    @abstractmethod
    def eval(self, dict):
        pass


class Var(Statement):
    pass


class Condition(ABC):
    @abstractmethod
    def test(self, dict):
        pass


class Bool(Condition):
    def __init__(self, bool: bool):
        self.bool = bool

    def test(self, dict):
        return bool


class DictVar(Var, Condition):
    def __init__(self, name: [str]):
        self.name = name

    def __repr__(self):
        return f'DicVar: {self.name}'

    def eval(self, dict):
        v = dict['variables']
        for x in self.name:
            if x in v:
                v = v[x]
            else:
                pass  # TODO: error handling
        return v

    def test(self, dict):
        v = dict['variables']
        for x in self.name:
            if x not in v:
                return False
            v = v[x]

        return True


class TmpVar(Var, Condition):
    def __init__(self, name: [str]):
        self.name = name

    def __repr__(self):
        return f'TmpVar: {self.name}'

    def eval(self, dict):
        tmp = dict['tmp']
        for x in self.name:
            tmp = tmp[x]
        return tmp

    def test(self, dict):
        tmp = dict['tmp']
        for x in self.name:
            if x not in tmp:
                return False
            tmp = tmp[x]

        return True


class Text(Var):
    def __init__(self, content: str):
        self.content = content

    def __repr__(self):
        return f'Text: \'{self.content}\''.encode('unicode_escape').decode('utf-8')

    def eval(self, eval):
        return self.content


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
            r += str(b.eval(dict))

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
        alias: Alias = dict['aliases'][self.alias_name]  # TODO: check if exists
        if len(self.args) != len(alias.vars):
            pass # TODO: erro

        new_dict = copy.deepcopy(dict)

        for (var, arg) in zip(alias.vars, self.args):
            new_dict['tmp'][var] = arg.eval(dict)

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
        for v in self.var.eval(dict):
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
