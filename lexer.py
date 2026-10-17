import ply.lex as lex

tokens = (
    'LET', 'FUNC', 'IF', 'ELSE', 'WHILE', 'FOR', 'RETURN', 'PRINT',
    'IDENTIFIER', 'INTEGER', 'FLOAT', 'STRING',
    'TRUE', 'FALSE',
    'PLUS', 'MINUS', 'TIMES', 'DIVIDE', 'MODULO',
    'EQUAL', 'NOTEQ', 'GREATERTHAN', 'LESSTHAN', 'LESSEQ', 'GREATEREQ',
    'LPAREN', 'RPAREN', 'LBRACE', 'RBRACE', 'COMMA', 'SEMICOLON', 'ASSIGN',
    'MEM_ANNOTATION'
)


# palabras q tienen un significado especial en el lenguaje.
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


# ignora los comentarios q empiezan con //.
def t_COMMENT(t):
    r'//[^\n]*'
    pass


# reconoce la anotacion @memory.
def t_MEM_ANNOTATION(t):
    r'@memory'
    return t


# reconoce palabras, como nombres de variables.
def t_IDENTIFIER(t):
    r'[a-zA-Z_][a-zA-Z0-9_]*'

    # si es una palabra reservada, cambia el tipo del token.
    if t.value in reserved:
        t.type = reserved[t.value]
    return t


# reconoce decimales como 3.14.
# va antes de INTEGER para reconocer el numero completo.
def t_FLOAT(t):
    r'[0-9]+\.[0-9]+'
    t.value = float(t.value)
    return t


# reconoce enteros como 3 o 100.
def t_INTEGER(t):
    r'[0-9]+'
    t.value = int(t.value)
    return t


# reconoce texto entre comillas dobles.
def t_STRING(t):
    r'"[^"\n]*"'

    # quita las comillas y guarda el texto de adentro.
    t.value = t.value[1:-1]
    return t


# operadores aritmeticos.
t_PLUS = r'\+'
t_MINUS = r'-'
t_TIMES = r'\*'
t_DIVIDE = r'/'
t_MODULO = r'%'

# operadores de comparacion.
t_EQUAL = r'=='
t_NOTEQ = r'!='
t_GREATERTHAN = r'>'
t_LESSTHAN = r'<'
t_LESSEQ = r'<='
t_GREATEREQ = r'>='

# parentesis, llaves y otros simbolos.
t_LPAREN = r'\('
t_RPAREN = r'\)'
t_LBRACE = r'\{'
t_RBRACE = r'\}'
t_COMMA = r','
t_SEMICOLON = r';'
t_ASSIGN = r'='

# ignora espacios, tabs y retornos de carro.
t_ignore = ' \t\r'


# cuenta los saltos de linea para reportar errores.
def t_newline(t):
    r'\n+'
    t.lexer.lineno += len(t.value)


# muestra el caracter q no pudo reconocer.
# detiene el analisis si encuentra un caracter no permitido.
def t_error(t):
    raise SyntaxError(
        f"Error: illegal character '{t.value[0]}' at line {t.lineno}"
    )


# construye el lexer con las reglas de arriba.
lexer = lex.lex()