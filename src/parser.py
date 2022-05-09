from ply import yacc
from lexer import Lexer
import sys

dic = {
    'coisas' : 'mais coisas',
    'cenas' : ['bue', 'de', 'cenas', 'juro', 'mano'],
    'welele' : {
        'yo' : ['eh', 'eh'],
        'ya' : 'oh boy'
    }
}

class Parser:
    def __init__(self, dic):
        self.dic = dic
        self.lexer = Lexer()
        self.tokens = self.lexer.tokens
        self.parser = yacc.yacc(module=self, write_tables=1)

    def parse(self, data):
        self.parser.parse(data)

    def p_lang(self, p):
        'lang : statements'
        p[0] = p[1]

    def p_statements(self, p):
        'statements : statements statement'
        p[0] = p[1] + p[2]

    def p_statements_empty(self, p):
        'statements : '
        p[0] = ""

    def p_statement_conditionals(self, p):
        'statement : if elifs else'
        if p[1]:
            p[0] = p[1]
        elif p[2]:
            p[0] = p[2]
        elif p[3]:
            p[0] = p[3]
        else:
            p[0] = ""

    def p_if(self, p):
        'if : IF VAR block'
        if p[2] in dic:
            p[0] = p[3]
        else:
            p[0] = ""

    def p_elifs(self, p):
        'elifs : elifs elif'
        if p[1]:
            p[0] = p[1]
        elif p[2]:
            p[0] = p[2]
        else:
            p[0] = ""

    def p_elif(self, p):
        'elif : ELIF VAR block'
        if p[2] in self.dic:
            p[0] = p[3]
        else:
            p[0] = ""

    def p_elifs_empty(self, p):
        'elifs : '
        p[0] = ""

    def p_else(self, p):
        'else : ELSE block'
        p[0] = p[2]

    def p_else_empty(self, p):
        'else : '
        p[0] = ""

    def p_statement_for(self, p):
        'statement : FOR TMPVAR ":" var block'
        p[0] = ""
        for x in p[4]:
            p[0] += p[5].strip().replace(p[2], x) + '\n'

    def p_block(self, p):
        'block : "{" statements "}"'
        p[0] = p[1]

    def p_statement_phrase(self, p):
        'statement : phrase NEWLINE'
        p[0] = p[1] + '\n'

    def p_phrase(self, p):
        'phrase : phrase word'
        spaces = ''
        if p[1]:
            spaces = ' '
        p[0] = p[1] + spaces + p[2]

    def p_phrase_empty(self, p):
        'phrase : '
        p[0] = ''

    def p_word(self, p):
        '''
        word : WORD
            | var
            | TMPVAR
        '''
        p[0] = p[1]

    def p_var(self, p):
        'var : VAR'
        tmp = dic
        for x in p[1]:
            tmp = tmp[x]
        p[0] = tmp

    def p_error(self, p):
        print("Syntax error: ", p)

file = open(sys.argv[1], "r")
content = file.read()

parser = Parser(dic)

result = parser.parse(content)

print(result)
