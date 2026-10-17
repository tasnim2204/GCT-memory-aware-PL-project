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