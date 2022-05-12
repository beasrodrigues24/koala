from ply import lex


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
    print(f'Lexer Error at: {t.lexer.lineno}:{t.lexer.lexpos}')
    t.lexer.skip(1)
    
lex.lex()