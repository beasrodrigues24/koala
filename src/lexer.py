from ply import lex 

tokens = ['VAR', 'TMPVAR', 'TEXT', 'IF', 'ELIF', 'ELSE', 'FOR']
literals = ['{', '}', ':']

t_ignore = ' \t\n'

def t_VAR(t):
    r'\$[A-Za-z_]\w*'
    t.value = t.value[1:]
    return t

def t_TMPVAR(t):
    r'\#[A-Za-z_]\w*'
    return t

def t_IF(t):
    r'@if'
    return t

def t_ELIF(t):
    r'@elif'
    return t

def t_ELSE(t):
    r'@else'
    return t 

def t_FOR(t):
    r'@for'
    return t

def t_TEXT(t):
    r'\w+'
    return t

def t_error(t):
    print('ERROR')
    t.lexer.skip(1)

lexer = lex.lex()