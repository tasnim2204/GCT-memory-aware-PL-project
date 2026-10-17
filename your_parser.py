import sys
from lexer import lexer

if len(sys.argv) != 2:
  print('Error: incorrect number of arguments\n')
  sys.exit(1)

filename = sys.argv[1]

try:
    with open(filename, 'r') as f:
        source = f.read()
except FileNotFoundError:
    print(f'Error: the file "{filename}" was not found.')
    sys.exit(1)

def p_error(p):
    if p:
        print(f"Error: unexpected token '{p.value}' at line {p.lineno}")
    else:
        print("Error: unexpected end of file")

lexer.input(source)

for tok in lexer:
    print(tok)