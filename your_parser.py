import sys
from pprint import pprint
from parserrules import parser, lexer


# verifica q escribimos el nombre del archivo en el comando.
# sys.argv[0] es your_parser.py y sys.argv[1] es el archivo.
if len(sys.argv) != 2:
    print("Uso: python your_parser.py archivo.uedge")
    sys.exit(1)

filename = sys.argv[1]


try:
    # abre el archivo y guarda su contenido en source.
    with open(filename, 'r', encoding='utf-8') as f:
        source = f.read()

    # comienza a contar las lineas desde 1.
    lexer.lineno = 1

    # el parser revisa el codigo y devuelve su estructura.
    result = parser.parse(source, lexer=lexer)
    # muestra el resultado organizado en varias lineas.
    print("Parser exitoso")
    pprint(result, width=80)

except FileNotFoundError:
    print(f'Error: no se encontro el archivo "{filename}".')
    sys.exit(1)

except PermissionError:
    print(f'Error: no tienes permiso para leer "{filename}".')
    sys.exit(1)

except UnicodeDecodeError:
    print(f'Error: el archivo "{filename}" no se pudo leer como UTF-8.')
    sys.exit(1)

except OSError as e:
    print(f'Error al leer "{filename}": {e}')
    sys.exit(1)

except SyntaxError as e:
    # muestra el error de sintaxis sin el traceback largo.
    print(e)
    sys.exit(1)