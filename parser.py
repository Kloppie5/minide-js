##
#
# Full "lexer"/"parser" system for javascript.
# Translates a string of javascript to an uldl tree.
#
##

import os
from slimit.parser import Parser as SlimitParser

class Parser ( object ) :

    # State enum
    STATE_START = 0

    def __init__ ( self ) :
        self.state = self.STATE_START
        pass

    def parse ( self, code ) :
        print("parse")
        parser = SlimitParser()
        tree = parser.parse(code)
        print(tree.to_ecma())

    def parse_file ( self, filename ) :
        if not os.path.isfile(filename) :
            print("File not found: " + filename)
            return
        with open( filename, "r" ) as f :
            code = f.read()
        self.parse(code)
