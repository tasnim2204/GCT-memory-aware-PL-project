import sys

if len(sys.argv) != 2:
  print('Error: incorrect number of arguments\n')
  sys.exit(1)

filename = sys.argv[1]

try:
  with open(filename, 'r') as f:
    text = f.read()
  print(text)
except FileNotFoundError:
  print(f'Error: the file "{filename}" was not found.')
  sys.exit(1)
except PermissionError:
  print(f'Error: you dont have permission to read "{filename}".')
  sys.exit(1)
except OSError as e:
  print(f'Error: could not read "{filename}": {e}')
  sys.exit(1)
