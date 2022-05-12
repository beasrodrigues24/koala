from ply import lex

class Lexer:

    def __init__(self):
        self.lexer = lex.lex(module=self, debug=False)

    reserved = {
        'if': 'IF',
        'elif' : 'ELIF',
        'else' : 'ELSE',
        'for' : 'FOR',
        'alias' : 'ALIAS',
        'include' : 'INCLUDE'
    }

    tokens = ['VAR', 'TEXT', 'NEWLINE', 'TMPVAR', 'ALIASNAME', 'DOLLAR'] + list(reserved.values())
    literals = ['{', '}', ':', '(', ')']

    t_ignore = ' \t'

    def t_VAR(self, t):
        r'\@[A-Za-z_]\w*(\.\w+)*'
        t.value = t.value[1:].split('.')
        return t

    def t_TMPVAR(self, t):
        r'\#[A-Za-z_]\w*'
        return t

    def t_TEXT(self, t):
        r'\"[^"]+\"'
        t.value = t.value[1:-1]
        t.lexer.lineno += t.value.count('\n')
        return t

    def t_NEWLINE(self, t):
        r'\n'
        t.lexer.lineno += 1

    def t_DOLLAR(self, t):
        r'\$'
        t.value = '\n'
        return t

    def t_ALIASNAME(self, t):
        r'\w+'
        t.type = self.reserved.get(t.value, 'ALIASNAME')
        return t

    def t_ANY_error(self, t):
        print('ERROR', t)
        t.lexer.skip(1)
