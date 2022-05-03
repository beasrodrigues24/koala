from ply import yacc 
from lexer import tokens
import sys

dic = {
    'coisas' : 'mais coisas',
    'cenas' : ['bue', 'de', 'cenas', 'juro', 'mano']
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

def p_statement_text(p):
    'statement : TEXT'
    p[0] = p[1]

def p_statement_var(p):
    'statement : VAR'
    if p[1] in dic:
        p[0] = dic[p[1]]
    else: 
        p[0] = "" # switch p erro

def p_statement_for(p):
    'statement : FOR TMPVAR ":" VAR "{" statements "}"'
    p[0] = ""
    for x in dic[p[4]]: 
        p[0] += p[6].replace(p[2], x)

def p_statement_tmpvar(p):
    'statement : TMPVAR'
    p[0] = p[1]

def p_error(p):
    print("Syntax error: " , p)

file = open(sys.argv[1], "r")
content = file.read()

parser = yacc.yacc()

parser.vars = {}

result = parser.parse(content)

print(result)

#output = open("output.txt", "w")
#output.write(result)