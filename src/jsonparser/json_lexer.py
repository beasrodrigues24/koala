from ply import lex

class JSONLexer:
    
    def __init__(self):
        self.lexer = lex.lex(module=self, debug=False)

    tokens = ['STRING', 'NUMBER', 'TRUE', 'FALSE', 'NULL']
    literals = ['{', '}', ',', ':', '[', ']']

    t_ignore = ' \t'

    def t_STRING(t):
        r'\"(\\"|[^"])*\"'
        t.value = t.value.replace('\\','')[1:-1]
        return t

    def t_TRUE(t):
        r'true'
        return t

    def t_FALSE(t):
        r'false'
        return t

    def t_NULL(t):
        r'null'
        return t

    def t_NUMBER(t):
        r'-?\d+(\.\d+)?([eE][-+]?\d+)?'
        return t

    def t_newline(t):
        r'\n+'
        t.lexer.lineno += len(t.value)

    def t_error(t):
        print(f'Invalid token: {t.value} at line {t.lexer.lineno}')
        t.lexer.skip(1)