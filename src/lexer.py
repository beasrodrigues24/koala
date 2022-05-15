from ply import lex
import re

from pretty_print import PrettyPrint

class Lexer:

    def __init__(self):
        self.lexer = lex.lex(module=self, debug=False)
        self.ignore_newline = False
        self.template_filepath = ''

    def set_template_filepath(self, template_filepath):
        self.template_filepath = template_filepath

    reserved = {
        'if': 'IF',
        'elif' : 'ELIF',
        'else' : 'ELSE',
        'for' : 'FOR',
        'alias' : 'ALIAS',
        'include' : 'INCLUDE',
    }

    pipes = {
        'first': 'PIPE_FIRST',
        'last': 'PIPE_LAST',
        'head': 'PIPE_HEAD',
        'tail': 'PIPE_TAIL',
    }

    tokens = ['VAR', 'TEXT', 'NEWLINE', 'TMPVAR', 'ALIASNAME'] + list(reserved.values()) + list(pipes.values())
    literals = ['{', '}', ':', '(', ')', ',']

    t_ignore = ' \t'

    def t_lbrace(self, t):
        r'{'
        t.type = '{'
        self.ignore_newline = True
        return t

    def t_rbrace(self, t):
        r'}'
        t.type = '}'
        self.ignore_newline = True
        return t

    def t_rcbrace(self, t):
        r'\)'
        t.type = ')'
        self.ignore_newline = True
        return t

    def t_VAR(self, t):
        r'\@[A-Za-z_]\w*(\.\w+)*'
        t.value = t.value[1:].split('.')
        self.ignore_newline = False
        return t

    def t_TMPVAR(self, t):
        r'\#[A-Za-z_]\w*(\.\w+)*'
        t.value = t.value[1:].split('.')
        self.ignore_newline = False
        return t

    def t_pipe(self, t):
        r'/\w+'
        t.type = self.pipes.get(t.value[1:], '')
        if t.type:
            return t
        else:
            self.t_ANY_error(t)

    def t_TEXT(self, t):
        r'\"(\\"|[^"])*\"'
        t.value = re.sub(r'\\(.)', lambda x: x.group(1), t.value[1:-1])
        t.lexer.lineno += t.value.count('\n')
        self.ignore_newline = False
        return t

    def t_NEWLINE(self, t):
        r'\n'
        t.lexer.lineno += 1
        if not self.ignore_newline:
            return t
        else:
            self.ignore_newline = False


    def t_ALIASNAME(self, t):
        r'\w+'
        t.type = self.reserved.get(t.value, 'ALIASNAME')
        self.ignore_newline = False
        return t

    def t_ANY_error(self, t):
        PrettyPrint.template_warn(
            f'Invalid token: \'{t.value[0]}\'. Skipping...'.encode('unicode_escape').decode('utf-8'),
            self.template_filepath,
            t.lexer.lineno
        )
        t.lexer.skip(1)
