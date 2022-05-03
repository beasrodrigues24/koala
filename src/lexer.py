from ply import lex 

tokens = ['VAR', 'WORD', 'NEWLINE', 'TMPVAR', 'IF', 'ELIF', 'ELSE', 'FOR']
literals = ['{', '}', ':']

t_ignore = ' \t'

def t_VAR(t):
    r'\$[A-Za-z_]\w*(\.\w+)*'
    t.value = t.value[1:].split('.')
    return t

def t_TMPVAR(t):
    r'\#[A-Za-z_]\w*'
    return t

def t_WORD(t):
    r'\w+'
    return t

def t_NEWLINE(t):
    r'\n'
    t.lexer.lineno += 1
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

def t_error(t):
    print('ERROR', t)
    t.lexer.skip(1)

lexer = lex.lex()