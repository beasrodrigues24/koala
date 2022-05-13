from ply import lex

class Lexer:

    def __init__(self):
        self.lexer = lex.lex(module=self, debug=False)
        self.ignore_newline = False

    reserved = {
        'if': 'IF',
        'elif' : 'ELIF',
        'else' : 'ELSE',
        'for' : 'FOR',
        'alias' : 'ALIAS',
        'include' : 'INCLUDE'
    }

    tokens = ['VAR', 'TEXT', 'NEWLINE', 'TMPVAR', 'ALIASNAME'] + list(reserved.values())
    literals = ['{', '}', ':', '(', ')']

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
        r'\#[A-Za-z_]\w*'
        self.ignore_newline = False
        return t

    def t_TEXT(self, t):
        r'\"[^"]+\"'
        t.value = t.value[1:-1]
        t.lexer.lineno += t.value.count('\n')
        self.ignore_newline = False
        return t

    def t_NEWLINE(self, t):
        r'\n'
        t.lexer.lineno += 1
        if self.ignore_newline: 
            t.value = ''
        self.ignore_newline = False
        return t

    def t_ALIASNAME(self, t):
        r'\w+'
        t.type = self.reserved.get(t.value, 'ALIASNAME')
        self.ignore_newline = False
        return t

    def t_ANY_error(self, t):
        print('Invalid token:', t.value)
        t.lexer.skip(1)
