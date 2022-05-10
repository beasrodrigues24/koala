from ply import lex

class Lexer:

    def __init__(self):
        self.lexer = lex.lex(module=self, debug=False)

    reserved = {
        'if': 'IF',
        'elif' : 'ELIF',
        'else' : 'ELSE',
        'for' : 'FOR'
    }        

    tokens = ['VAR', 'TEXT', 'NEWLINE', 'TMPVAR', 'ALIAS'] + list(reserved.values())
    literals = ['{', '}', ':']

    t_ignore = ' \t'

    def t_VAR(self, t):
        r'\$[A-Za-z_]\w*(\.\w+)*'
        t.value = t.value[1:].split('.')
        return t

    def t_TMPVAR(self, t):
        r'\#[A-Za-z_]\w*'
        return t

    def t_TEXT(self, t):
        r'\".*\"'
        t.value = t.value[1:-1]
        return t

    def t_NEWLINE(self, t):
        r'\n'
        t.lexer.lineno += 1
        return t

    def t_ALIAS(self, t):
        r'\w+'
        t.type = self.reserved.get(t.value, 'ALIAS')
        return t

    def t_error(self, t):
        print('ERROR', t)
        t.lexer.skip(1)
