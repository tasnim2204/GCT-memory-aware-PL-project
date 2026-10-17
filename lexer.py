import ply.lex as lex

tokens = ('LET', 'FUNC', 'IF', 'ELSE', 'WHILE', 'FOR', 'RETURN', 'PRINT',         # KEYWORDS
          'IDENTIFIER', 'INTEGER', 'FLOAT', 'STRING',                             # IDENTIFIERS & DATA TYPES
          'TRUE', 'FALSE',                                                        # BOOLEAN
          'PLUS', 'MINUS', 'TIMES', 'DIVIDE', 'MODULO',                           # ARITHMETIC
          'EQUAL', 'NOTEQ', 'GREATERTHAN', 'LESSTHAN', 'LESSEQ', 'GREATEREQ',     # COMPARISON
          'LPAREN', 'RPAREN', 'LBRACE', 'RBRACE', 'COMMA', 'SEMICOLON', 'ASSIGN', # PUNCTUATION
          'MEM_ANNOTATION',                                                       # @memory
          'MEM_KEYWORD', 'PRECISION_TYPE')                                        # (alloc, free, deref, ref, gc, null, void) & (int8, float16)

reserved = {
    'if':     'IF',
    'else':   'ELSE',
    'while':  'WHILE',
    'for':    'FOR',
    'return': 'RETURN',
    'print':  'PRINT',
    'true':   'TRUE',
    'false':  'FALSE'
}

mem_keywords = {
    'alloc', 'free', 'deref', 'ref', 'gc', 'null', 'void'
}

precision_types = {
    'int8', 'float16'
}

def t_COMMENT(t):
    r'//[^\n]*'
    pass

def t_MEM_ANNOTATION(t):
    r'@memory|alloc|free|deref|ref|gc|null|void'
    return t

def t_IDENTIFIER(t):
    r'[a-zA-Z_][a-zA-Z0-9_]*'
    #check if it's a reserved word
    if t.value in reserved:
        t.type = reserved[t.value]
    #check if it's a mem_keyword
    elif t.value in mem_keywords:
        t.type = 'MEM_KEYWORD'
    elif t.value in precision_types:
        t.type = 'PRECISION_TYPE'
    return t

def t_INTEGER(t):
    r'[0-9_]+'
    t.value = int(t.value)
    return t

def t_FLOAT(t):
    r'\d-\.\d+'
    t.value = float(t.value)
    return t

def t_STRING(t):
    r'"[^"\n]*"'
    t.value = t.value[1:-1]

t_LET = r'let'
t_FUNC = r'func'

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
    print(f"Error: illegal character '{t.value[0]}' at line {t.lineno}")    
    t.lexer.skip(1)

lexer = lex.lex()