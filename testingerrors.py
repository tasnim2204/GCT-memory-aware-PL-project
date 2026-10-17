from parserrules import parser, lexer


# este archivo prueba diferentes errores por separado.
# cada caso tiene un nombre y un ejemplo de codigo incorrecto.
# esperamos q el parser rechace cada ejemplo.
tests = [
    ("falta punto y coma", "let a = 3"),
    ("falta nombre de variable", "let = 3;"),
    ("falta signo igual", "let a 3;"),
    ("falta expresion", "let a = ;"),
    ("falta cerrar parentesis", "print(3;"),
    ("operacion incompleta", "print(2 + );"),
    ("sobra un parentesis", "print(3));"),
    ("caracter no permitido", "let a = 3$;"),
        # --- multi-line tests: verify line numbers are correct ---
    ("multilinea: error en linea 3", "let a = 3;\nlet b = 5;\nlet c = ;"),
    ("multilinea: error en linea 5", "let a = 3;\nlet b = 5;\nlet c = 7;\nlet d = 9;\nlet e = ;"),
    ("multilinea: llave sin cerrar", "func f() {\n  let a = 3;\nprint(a);"),

    # --- invalid tests for YOUR rules ---
    ("func sin cerrar parentesis", "func f(a, b {\n  return a;\n}"),
    ("if sin parentesis", "if a > b {\n  print(1);\n}"),
    ("while sin condicion", "while {\n  print(1);\n}"),
    ("return sin punto y coma", "func f() {\n  return 5\n}"),
    ("@memory sin parentesis", "@memory 40kb\nfunc f() {\n  print(1);\n}"),
    ("@memory sin cerrar parentesis", "@memory(40kb\nfunc f() {\n  print(1);\n}"),
    ("func sin llave de cierre", "func f() {\n  let a = 3;\n"),
]

# cuenta las pruebas q detectaron el error.
passed = 0


# revisa un caso a la vez.
for name, source in tests:
    print("\nPrueba:", name)
    print("Codigo:", source)

    # reinicia el numero de linea para cada prueba.
    lexer.lineno = 1

    try:
        # intenta analizar el codigo de este caso.
        parser.parse(source, lexer=lexer)

    except SyntaxError as error:
        # detectar el error es lo q esperamos en estas pruebas.
        print("PASS: rechazo el codigo incorrecto.")
        print("Detalle:", error)
        passed = passed + 1

    else:
        # si no lanzo un error, el caso no fue rechazado.
        print("FAIL: termino sin rechazar el codigo incorrecto.")


# muestra cuantas pruebas pasaron.
print("\nResultado:", passed, "de", len(tests), "pruebas pasaron.")