from fileinput import filename
from ply import yacc
from lexer import Lexer
from pretty_print import PrettyPrint

class Parser:
    def __init__(self, dic):
        self.dic = dic
        self.lexer = Lexer()
        self.tokens = self.lexer.tokens
        self.parser = yacc.yacc(module=self, write_tables=1)
        self.aliases = {}
        self.data = ''
        self.template_filepath = ''

    def load_template(self, filepath):
        self.template_filepath = filepath
        try:
            self.data = open(filepath, 'r').read()
        except IOError:
            PrettyPrint.error(f'File {filepath} not found.')
            exit(1)

    def parse(self):
        return self.parser.parse(self.data)

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
        if p[2] in self.dic:
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
            p[0] = ''

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
        'statement : FOR TMPVAR ":" variable block'
        p[0] = ""
        for x in p[4]:
            p[0] += p[5].replace(p[2], x)

    def p_statement_alias(self, p):
        'statement : ALIAS ALIASNAME tmpvars block'
        self.aliases[p[2]] = {
            'vars' : p[3],
            'content' : p[4]
        }
        p[0] = ''

    def p_statement_include(self, p):
        'statement : INCLUDE TEXT NEWLINE'
        include_parser = Parser(self.dic)
        include_parser.load_template(p[2])
        include_parser.parse()
        self.aliases.update(include_parser.aliases)
        p[0] = ''

    def p_tmpvars(self, p):
        'tmpvars : tmpvars TMPVAR'
        p[0] = p[1] + [p[2]]

    def p_tmpvars_empty(self, p):
        'tmpvars : '
        p[0] = []

    def p_block(self, p):
        'block : "{" statements "}"'
        p[0] = p[2]

    def p_statement_text(self, p):
        'statement : text'
        p[0] = p[1]

    def p_text_text(self, p):
        'text : TEXT'
        p[0] = p[1]

    def p_text_variable(self, p):
        'text : variable'
        p[0] = p[1]

    def p_text_newline(self, p):
        'text : NEWLINE'
        p[0] = p[1]

    def p_text_callalias(self, p):
        'text : ALIASNAME  "(" variable ")"'
        tmp = ''
        if p[1] in self.aliases:
            for tmpvar in self.aliases[p[1]]['vars']:
                tmp += self.aliases[p[1]]['content'].replace(tmpvar, p[3])
            p[0] = tmp
        else:
            PrettyPrint.template_error(f'Alias {p[1]} not defined.', self.template_filepath, p.lineno(1))
            exit(1)

    def p_variable_var(self, p):
        'variable : VAR'
        tmp = self.dic
        for x in p[1]:
            tmp = tmp[x]
        p[0] = tmp

    def p_variable_tmpvar(self, p):
        'variable : TMPVAR'
        p[0] = p[1]

    def p_error(self, p):
        PrettyPrint.template_error(
            f'Syntax error. Token \'{p.value}\' not expected.'.encode("unicode_escape").decode("utf-8"),
            self.template_filepath,
            p.lexer.lineno
        )
        exit(1)
