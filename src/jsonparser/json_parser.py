from ply import yacc
from json_lexer import tokens

def p_json(p):
    'json : element'
    p[0] = p[1]

def p_value(p):
    '''
        value : object
        value : array
        value : STRING
        value : NUMBER
        value : TRUE
        value : FALSE
        value : NULL
    '''
    p[0] = p[1]
    
def p_object_empty(p):
    'object : "{" "}"'
    p[0] = []
    
def p_object_members(p):
    'object : "{" members "}"'
    p[0] = p[2]
    
def p_members_single(p):
    'members : member'
    p[0] = p[1]
    
 #   {"a" : 4}
    
def p_members_multiple(p):
    'members : members "," member'
    p[1].update(p[3])
    p[0] = p[1]
    
  #  { "a":4, "b": 5, "c":6}
    
def p_member(p):
    'member : STRING ":" element'
    #print(p[1], p[3])
    p[0] = {p[1] : p[3]}
    
def p_array_empty(p):
    'array : '
    p[0] = []
    
def p_array_elements(p):
    'array : "[" elements "]"'
    p[0] = p[2]
    
   # [{"a" : 2}, {"b" : 4}]
    
def p_elements_single(p):
    'elements : element'
    p[0] = [p[1]]
    
def p_elements_multiple(p):
    'elements : elements "," element'
    p[0] = p[1] + [p[3]]
    
def p_element(p):
    'element : value'
    p[0] = p[1]
    
def p_error(p):
    #print('Syntax Error.')
    #exit()
    pass

file = open('/home/tgvp/Documents/Universidade/PL/Aula02/cinemaATP.json', 'r').read()
parser = yacc.yacc()

result = parser.parse(file)

print(result)