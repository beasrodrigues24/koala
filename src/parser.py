from ply import yacc 
from lexer import tokens
import sys

dic = {
    'coisas' : 'mais coisas',
    'cenas' : ['bue', 'de', 'cenas', 'juro', 'mano'],
    'welele' : {
        'yo' : ['eh', 'eh'],
        'ya' : 'oh boy'
    }
}

def p_lang(p):
    'lang : statements'
    p[0] = p[1]

def p_statements(p):
    'statements : statements statement'
    p[0] = p[1] + p[2]

def p_statements_empty(p):
    'statements : '
    p[0] = ""

def p_statement_conditionals(p):
    'statement : if elifs else'
    if p[1]:
        p[0] = p[1]
    elif p[2]:
        p[0] = p[2]
    elif p[3]:
        p[0] = p[3]
    else: 
        p[0] = ""
    
def p_if(p):
    'if : IF VAR "{" statements "}"'
    if p[2] in dic: 
        p[0] = p[4]
    else:
        p[0] = ""

def p_elifs(p):
    'elifs : elifs elif'
    if p[1]:
        p[0] = p[1]
    elif p[2]:
        p[0] = p[2]
    else:
        p[0] = ""

def p_elifs_empty(p):
    'elifs : '
    p[0] = ""

def p_elif(p):
    'elif : ELIF VAR "{" statements "}"'
    if p[2] in dic: 
        p[0] = p[4]
    else:
        p[0] = ""

def p_else(p):
    'else : ELSE "{" statements "}"'
    p[0] = p[3]

def p_else_empty(p):
    'else : '
    p[0] = ""

def p_statement_phrase(p):
    'statement : phrase NEWLINE'
    p[0] = p[1] + '\n'

def p_phrase(p): 
    'phrase : phrase word'
    spaces = ''
    if p[1]:
        spaces = ' '
    p[0] = p[1] + spaces + p[2] 

def p_phrase_empty(p):
    'phrase : '
    p[0] = ''

def p_word(p):
    '''
    word : WORD
         | var
         | TMPVAR
    '''
    p[0] = p[1]

def p_var(p):
    'var : VAR'
    tmp = dic
    for x in p[1]:
        tmp = tmp[x]
    p[0] = tmp
    
def p_statement_for(p):
    'statement : FOR TMPVAR ":" var "{" statements "}"'
    p[0] = ""
    for x in p[4]: 
        p[0] += p[6].strip().replace(p[2], x) + '\n'

def p_error(p):
    print("Syntax error: ", p)

file = open(sys.argv[1], "r")
content = file.read()

parser = yacc.yacc()

result = parser.parse(content)

print(result)

#output = open("output.txt", "w")
#output.write(result)