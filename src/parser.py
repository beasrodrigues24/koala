from ply import yacc
from lexer import Lexer
from pretty_print import PrettyPrint
from koala_ast.variables import DictVar, TmpVar, Text, Field, Pipe
from koala_ast.statements import Block, Alias, CallAlias, For, If, Ifs
from koala_ast.conditions import Bool

class Parser:
    def __init__(self):
        self.lexer = Lexer()
        self.tokens = self.lexer.tokens
        self.parser = yacc.yacc(module=self, write_tables=1)
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
        p[0] = Block(p[1])

    def p_statements(self, p):
        'statements : statements statement'
        p[0] = p[1] + [p[2]]

    def p_statements_empty(self, p):
        'statements : '
        p[0] = []

    def p_statement_variable(self, p):
        'statement : variable'
        p[0] = p[1]

    def p_statement_newline(self, p):
        'statement : NEWLINE'
        if p[1] != '':
            p[0] = Text(p[1])

    def p_statement_conditionals(self, p):
        'statement : if elifs else'
        p[0] = Ifs(p[1] + p[2] + p[3])

    def p_if(self, p):
        'if : IF variable block'
        p[0] = [If(p[2], p[3])]

    def p_elifs(self, p):
        'elifs : elifs elif'
        p[0] = p[1] + [p[2]]

    def p_elif(self, p):
        'elif : ELIF variable block'
        p[0] = If(p[2], p[3])

    def p_elifs_empty(self, p):
        'elifs : '
        p[0] = []

    def p_else(self, p):
        'else : ELSE block'
        p[0] = [If(Bool(True), p[2])]

    def p_else_empty(self, p):
        'else : '
        p[0] = []

    def p_statement_for(self, p):
        'statement : FOR TMPVAR ":" variable block'
        # if '.' in p[2]:
        #     PrettyPrint.template_warn(
        #         '\'.\' found in temporary variable declaration, ignoring following qualifiers...',
        #         self.template_filepath,
        #         p.lineno(2)
        #     )
        p[0] = For(p[2], p[4], p[5])

    def p_statement_alias(self, p):
        'statement : ALIAS ALIASNAME tmpvars block'
        # tmpvars = []
        # for tmpvar in p[3]:
        #     if '.' in tmpvar:
        #         PrettyPrint.template_warn(
        #             '\'.\' found in temporary variable declaration, ignoring following qualifiers...',
        #             self.template_filepath,
        #             p.lineno(3)
        #         )
        #     tmpvars += [tmpvar[0]]
        p[0] = Alias(p[2], p[3], p[4])

    def p_tmpvars(self, p):
        'tmpvars : tmpvars TMPVAR'
        p[0] = p[1] + [p[2]]

    def p_tmpvars_empty(self, p):
        'tmpvars : '
        p[0] = []

    def p_statement_callalias(self, p):
        'statement : ALIASNAME  "(" args ")"'
        p[0] = CallAlias(p[1], p[3])

    def p_args(self, p):
        'args : variables'
        p[0] = p[1]

    def p_args_empty(self, p):
        'args : '
        p[0] = []

    def p_variables(self, p):
        'variables : variables "," variable'
        p[0] = p[1] + [p[3]]

    def p_variables_single(self, p):
        'variables : variable'
        p[0] = [p[1]]

    def p_statement_include(self, p):
        'statement : INCLUDE TEXT NEWLINE'
        include_parser = Parser()
        include_parser.load_template(p[2])
        p[0] = Block(include_parser.parse())

    def p_block(self, p):
        'block : "{" statements "}"'
        p[0] = Block(p[2])

    def p_variable_var(self, p):
        'variable : VAR'
        p[0] = DictVar(p[1])

    def p_variable_tmpvar(self, p):
        'variable : TMPVAR'
        p[0] = TmpVar(p[1])

    def p_variable_text(self, p):
        'variable : TEXT'
        p[0] = Text(p[1])

    def p_variable_field(self, p):
        'variable : variable FIELD'
        p[0] = Field(p[1], p[2])

    def p_variable_pipe(self, p):
        'variable : variable PIPE'
        p[0] = Pipe(p[1], p[2])

    def p_error(self, p):
        PrettyPrint.template_error(
            f'Syntax error. Token \'{p.value}\' not expected.'.encode(
                'unicode_escape').decode('utf-8'),
            self.template_filepath,
            p.lexer.lineno
        )
        exit(1)
