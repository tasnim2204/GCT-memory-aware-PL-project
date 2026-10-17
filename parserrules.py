import ply.yacc as yacc
from lexer import tokens, lexer


# indica q operaciones se agrupan primero.
# las de abajo tienen mas prioridad:
# multiplicar y dividir antes q sumar y restar.
precedence = (
    ('nonassoc', 'EQUAL', 'NOTEQ', 'LESSTHAN',
     'GREATERTHAN', 'LESSEQ', 'GREATEREQ'),
    ('left', 'PLUS', 'MINUS'),
    ('left', 'TIMES', 'DIVIDE', 'MODULO'),
)


# un programa contiene una lista de instrucciones.
def p_program(p):
    'program : statements'
    p[0] = p[1]


# si solo hay una instruccion, crea una lista con ella.
def p_statements_one(p):
    'statements : statement'
    p[0] = [p[1]]


# si hay mas instrucciones, añade la nueva a la lista.
def p_statements_many(p):
    'statements : statements statement'
    p[0] = p[1] + [p[2]]


# por ahora reconocemos estos tres tipos de instrucciones.
# despues conectamos aqui las otras reglas del equipo.
def p_statement(p):
    '''statement : declaration
                 | assignment
                 | print_statement'''
    p[0] = p[1]


# reconoce una declaracion como: let a = 3;
def p_declaracion(p):
    'declaration : LET IDENTIFIER ASSIGN expression SEMICOLON'

    # guarda el tipo de instruccion, nombre y expresion.
    # para let a = 3; queda ('declaration', 'a', 3).
    p[0] = ('declaration', p[2], p[4])


# reconoce una asignacion como: a = 8;
def p_assignment(p):
    'assignment : IDENTIFIER ASSIGN expression SEMICOLON'

    # guarda el nombre de la variable y la nueva expresion.
    # aqui no estamos cambiando el valor de una variable real.
    p[0] = ('assignment', p[1], p[3])


# reconoce una instruccion como: print(a);
def p_print_statement(p):
    'print_statement : PRINT LPAREN expression RPAREN SEMICOLON'

    # guarda lo q el programa quiere imprimir.
    # el parser no ejecuta ese print.
    p[0] = ('print', p[3])


# reconoce un numero entero como expresion.
def p_expression_integer(p):
    'expression : INTEGER'

    # el lexer ya convirtio el numero a int.
    p[0] = p[1]


# reconoce un numero decimal como expresion.
def p_expression_float(p):
    'expression : FLOAT'
    p[0] = p[1]


# reconoce texto como: "hello".
def p_expression_string(p):
    'expression : STRING'
    p[0] = p[1]


# reconoce true del lenguaje UEDGE.
def p_expression_true(p):
    'expression : TRUE'
    p[0] = True


# reconoce false del lenguaje UEDGE.
def p_expression_false(p):
    'expression : FALSE'
    p[0] = False


# reconoce el nombre de una variable como expresion.
def p_expression_identifier(p):
    'expression : IDENTIFIER'

    # guarda el nombre; no busca su valor todavia.
    p[0] = ('identifier', p[1])


# reconoce operaciones con una expresion a cada lado.
# ejemplos: a + 3, 5 * 2, a < 10.
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

    # p[1] = expresion de la izquierda.
    # p[2] = operador, como + o *.
    # p[3] = expresion de la derecha.
    # guardamos la estructura sin calcular el resultado.
    p[0] = ('binary', p[2], p[1], p[3])


# reconoce una expresion entre parentesis, como (2 + 3).
def p_expression_parentheses(p):
    'expression : LPAREN expression RPAREN'

    # conserva la expresion q esta dentro.
    p[0] = p[2]


# se llama cuando los tokens no siguen las reglas.
def p_error(p):
    if p is not None:
        raise SyntaxError(
            f"Error: unexpected token '{p.value}' at line {p.lineno}"
        )
    else:
        raise SyntaxError(
            f"Error: unexpected end of file at line {lexer.lineno}"
        )


# construye el parser usando las reglas de este archivo.
# program es la regla donde comienza a revisar.
parser = yacc.yacc(
    start='program',
    write_tables=False,
    debug=False
)