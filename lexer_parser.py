import sys
sys.path.insert(0, 'ply.zip')
import ply.lex as lex
import ply.yacc as yacc

# LEXER
tokens = (
    'LET', 'FUNC', 'IF', 'ELSE', 'WHILE', 'FOR', 'RETURN', 'PRINT',
    'IDENTIFIER', 'INTEGER', 'FLOAT', 'STRING',
    'TRUE', 'FALSE',
    'PLUS', 'MINUS', 'TIMES', 'DIVIDE', 'MODULO',
    'EQUAL', 'NOTEQ', 'GREATERTHAN', 'LESSTHAN', 'LESSEQ', 'GREATEREQ',
    'LPAREN', 'RPAREN', 'LBRACE', 'RBRACE', 'COMMA', 'SEMICOLON', 'ASSIGN',
    'MEM_ANNOTATION'
)

reserved = {
    'let':    'LET',
    'func':   'FUNC',
    'if':     'IF',
    'else':   'ELSE',
    'while':  'WHILE',
    'for':    'FOR',
    'return': 'RETURN',
    'print':  'PRINT',
    'true':   'TRUE',
    'false':  'FALSE'
}

def t_COMMENT(t):
    r'//[^\n]*'
    pass

def t_MEM_ANNOTATION(t):
    r'@memory'
    return t

def t_IDENTIFIER(t):
    r'[a-zA-Z_][a-zA-Z0-9_]*'
    if t.value in reserved:
        t.type = reserved[t.value]
    return t

def t_FLOAT(t):
    r'[0-9]+\.[0-9]+'
    t.value = float(t.value)
    return t

def t_INTEGER(t):
    r'[0-9]+'
    t.value = int(t.value)
    return t

def t_STRING(t):
    r'"[^"\n]*"'
    t.value = t.value[1:-1]
    return t

# catches strings that aren't closed with ""
def t_unterminated_string(t):
    r'"[^"\n]*'
    print(f"Error: malformed string at line {t.lexer.lineno}")
    sys.exit(0) # clean exit to avoid getting flagged as runtime error

t_PLUS = r'\+'
t_MINUS = r'-'
t_TIMES = r'\*'
t_DIVIDE = r'/'
t_MODULO = r'%'

t_EQUAL = r'=='
t_NOTEQ = r'!='
t_GREATERTHAN = r'>'
t_LESSTHAN = r'<'
t_LESSEQ = r'<='
t_GREATEREQ = r'>='

t_LPAREN = r'\('
t_RPAREN = r'\)'
t_LBRACE = r'\{'
t_RBRACE = r'\}'
t_COMMA = r','
t_SEMICOLON = r';'
t_ASSIGN = r'='

t_ignore = ' \t\r'

def t_newline(t):
    r'\n+'
    t.lexer.lineno += len(t.value)

def t_error(t):
    print(f"Error: unexpected token '{t.value[0]}' at line {t.lexer.lineno}")
    sys.exit(0)

# PARSER
precedence = (
    ('nonassoc', 'EQUAL', 'NOTEQ', 'LESSTHAN', 'GREATERTHAN', 'LESSEQ', 'GREATEREQ'),
    ('left', 'PLUS', 'MINUS'),
    ('left', 'TIMES', 'DIVIDE', 'MODULO'),
)

def p_program(p):
    'program : statements'
    p[0] = p[1]

def p_statements_one(p):
    'statements : statement'
    p[0] = [p[1]]

def p_statements_many(p):
    'statements : statements statement'
    p[0] = p[1] + [p[2]]

def p_statement(p):
    '''statement : declaration
                 | assignment
                 | print_statement
                 | func_decl
                 | annotated_func
                 | if_statement
                 | while_statement
                 | for_statement
                 | return_statement
                 | call_statement
                 | block'''
    p[0] = p[1]

def p_block(p):
    'block : LBRACE statements RBRACE'
    p[0] = ('block', p[2])

def p_declaracion(p):
    'declaration : LET IDENTIFIER ASSIGN expression SEMICOLON'
    p[0] = ('declaration', p[2], p[4])

def p_assignment(p):
    'assignment : IDENTIFIER ASSIGN expression SEMICOLON'
    p[0] = ('assignment', p[1], p[3])

def p_print_statement(p):
    'print_statement : PRINT LPAREN expression RPAREN SEMICOLON'
    p[0] = ('print', p[3])


def p_mem_annotation(p):
    '''mem_annotation : MEM_ANNOTATION LPAREN INTEGER IDENTIFIER RPAREN
                      | MEM_ANNOTATION LPAREN INTEGER RPAREN'''
    unit = p[4] if len(p) == 6 else None
    p[0] = ('mem_annotation', p[3], unit)
    
def p_mem_annotation_error(p):
    'mem_annotation : MEM_ANNOTATION LPAREN RPAREN'
    print(f"Error: malformed @memory annotation at line {p.lineno(1)}")
    sys.exit(0)

def p_annotated_func(p):
    'annotated_func : mem_annotation func_decl'
    p[0] = ('annotated_func', p[1], p[2])

def p_func_decl(p):
    'func_decl : FUNC IDENTIFIER LPAREN param_list_opt RPAREN LBRACE statements RBRACE'
    p[0] = ('func', p[2], p[4], p[7])

def p_param_list_opt_empty(p):
    'param_list_opt : '
    p[0] = []

def p_param_list_opt_nonempty(p):
    'param_list_opt : param_list'
    p[0] = p[1]

def p_param_list_one(p):
    'param_list : IDENTIFIER'
    p[0] = [p[1]]

def p_param_list_many(p):
    'param_list : param_list COMMA IDENTIFIER'
    p[0] = p[1] + [p[3]]

def p_if_statement(p):
    '''if_statement : IF LPAREN expression RPAREN LBRACE statements RBRACE
                    | IF LPAREN expression RPAREN LBRACE statements RBRACE ELSE LBRACE statements RBRACE'''
    if len(p) == 8:
        p[0] = ('if', p[3], p[6], None)
    else:
        p[0] = ('if', p[3], p[6], p[10])

def p_while_statement(p):
    'while_statement : WHILE LPAREN expression RPAREN LBRACE statements RBRACE'
    p[0] = ('while', p[3], p[6])

def p_for_statement(p):
    '''for_statement : FOR LPAREN LET IDENTIFIER ASSIGN expression SEMICOLON expression SEMICOLON IDENTIFIER ASSIGN expression RPAREN LBRACE statements RBRACE'''
    init = ('declaration', p[4], p[6])
    update = ('assignment', p[10], p[12])
    p[0] = ('for', init, p[8], update, p[15])

def p_return_statement(p):
    '''return_statement : RETURN expression SEMICOLON
                        | RETURN SEMICOLON'''
    p[0] = ('return', p[2] if len(p) == 4 else None)

def p_call_statement(p):
    'call_statement : IDENTIFIER LPAREN arg_list_opt RPAREN SEMICOLON'
    p[0] = ('call', p[1], p[3])

def p_arg_list_opt_empty(p):
    'arg_list_opt : '
    p[0] = []

def p_arg_list_opt_nonempty(p):
    'arg_list_opt : arg_list'
    p[0] = p[1]

def p_arg_list_one(p):
    'arg_list : expression'
    p[0] = [p[1]]

def p_arg_list_many(p):
    'arg_list : arg_list COMMA expression'
    p[0] = p[1] + [p[3]]

# ---- expressions ----
def p_expression_call(p):
    'expression : IDENTIFIER LPAREN arg_list_opt RPAREN'
    p[0] = ('call', p[1], p[3])

def p_expression_integer(p):
    'expression : INTEGER'
    p[0] = p[1]

def p_expression_float(p):
    'expression : FLOAT'
    p[0] = p[1]

def p_expression_string(p):
    'expression : STRING'
    p[0] = p[1]

def p_expression_true(p):
    'expression : TRUE'
    p[0] = True

def p_expression_false(p):
    'expression : FALSE'
    p[0] = False

def p_expression_identifier(p):
    'expression : IDENTIFIER'
    p[0] = ('identifier', p[1])

def p_expression_operation(p):
    '''expression : expression PLUS expression
                  | expression MINUS expression
                  | expression TIMES expression
                  | expression DIVIDE expression
                  | expression MODULO expression
                  | expression EQUAL expression
                  | expression NOTEQ expression
                  | expression LESSTHAN expression
                  | expression GREATERTHAN expression
                  | expression LESSEQ expression
                  | expression GREATEREQ expression'''
    p[0] = ('binary', p[2], p[1], p[3])

def p_expression_parentheses(p):
    'expression : LPAREN expression RPAREN'
    p[0] = p[2]


# ERROR HANDLING

def p_error(p):
    if p is None:
        print("Error: missing closing '}'")
        sys.exit(0)
    
    val = p.value
    tok_type = p.type
    
    # 1. Missing Semicolon Logic
    if tok_type in ('PRINT', 'LET', 'IF', 'WHILE', 'FOR', 'RETURN', 'FUNC'):
        # check if it's line 1, else it's the previous line
        err_line = p.lineno - 1 if p.lineno > 1 else p.lineno
        print(f"Error: expected ';' at line {err_line}")
    
    # 2. Missing Close Parenthesis
    elif tok_type == 'LBRACE' and val == '{':
         print(f"Error: missing closing ')' at line {p.lineno}")
         
    # 3. Standard unexpected token
    else:
        print(f"Error: unexpected token '{val}' at line {p.lineno}")
    
    sys.exit(0)


def main():
    if len(sys.argv) != 2:
        print("Usage: python your_parser.py <file.uedge>")
        sys.exit(1)

    filename = sys.argv[1]
    try:
        with open(filename, 'r', encoding='utf-8') as f:
            source = f.read()
    except FileNotFoundError:
        print(f"Error: File '{filename}' not found.")
        sys.exit(1)

    lexer = lex.lex()
    parser = yacc.yacc(start='program')

    try:
        lexer.lineno = 1
        result = parser.parse(source, lexer=lexer)
        
        # If parse succeeded, print success message
        print("Parsed successfully")
        sys.exit(0)
    except Exception as e:
        # Fallback in case of unexpected internal PLY errors
        print(f"Error: internal parse error - {e}")
        sys.exit(0)

if __name__ == '__main__':
    main()