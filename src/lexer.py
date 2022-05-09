from ply import lex

class Lexer:

    def __init__(self):
        self.lexer = lex.lex(module=self, debug=False)

    tokens = ['VAR', 'WORD', 'NEWLINE', 'TMPVAR', 'IF', 'ELIF', 'ELSE', 'FOR']
    literals = ['{', '}', ':']

    t_ignore = ' \t'

    def t_VAR(self, t):
        r'\$[A-Za-z_]\w*(\.\w+)*'
        t.value = t.value[1:].split('.')
        return t

    def t_TMPVAR(self, t):
        r'\#[A-Za-z_]\w*'
        return t

    def t_WORD(self, t):
        r'\w+'
        return t

    def t_NEWLINE(self, t):
        r'\n'
        t.lexer.lineno += 1
        return t

    def t_IF(self, t):
        r'@if'
        return t

    def t_ELIF(self, t):
        r'@elif'
        return t

    def t_ELSE(self, t):
        r'@else'
        return t

    def t_FOR(self, t):
        r'@for'
        return t

    def t_error(self, t):
        print('ERROR', t)
        t.lexer.skip(1)
