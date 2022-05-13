from ply import yacc
from .json_lexer import JSONLexer

class JSONParser:
    def __init__(self):
        self.lexer = JSONLexer()
        self.tokens = self.lexer.tokens
        self.parser = yacc.yacc(module=self, write_tables=1)
        
    def load(self, data):
        return self.parser.parse(data)

    def p_json(self, p):
        'json : element'
        p[0] = p[1]

    def p_value(self, p):
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

    def p_object_empty(self, p):
        'object : "{" "}"'
        p[0] = []

    def p_object_members(self, p):
        'object : "{" members "}"'
        p[0] = p[2]

    def p_members_single(self, p):
        'members : member'
        p[0] = p[1]

    def p_members_multiple(self, p):
        'members : members "," member'
        p[1].update(p[3])
        p[0] = p[1]

    def p_member(self, p):
        'member : STRING ":" element'
        p[0] = {p[1] : p[3]}

    def p_array_empty(self, p):
        'array : '
        p[0] = []

    def p_array_elements(self, p):
        'array : "[" elements "]"'
        p[0] = p[2]

    def p_elements_single(self, p):
        'elements : element'
        p[0] = [p[1]]

    def p_elements_multiple(self, p):
        'elements : elements "," element'
        p[0] = p[1] + [p[3]]

    def p_element(self, p):
        'element : value'
        p[0] = p[1]

    def p_error(self, p):
        print('Syntax Error.')
        exit()