
import sys
from parser import Parser

if len(sys.argv) != 2:
    print("Usage: main.py <file>")
    sys.exit(1)

parser = Parser()
parser.parse_file(sys.argv[1])
