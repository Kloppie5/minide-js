##
#
# Full "lexer"/"parser" system for javascript.
# Translates a string of javascript to an uldl tree.
#
##

import os
from slimit.parser import Parser as SlimitParser
import slimit.ast

class Parser ( object ) :

    # State enum
    STATE_START = 0

    def __init__ ( self ) :
        self.state = self.STATE_START
        self.volatile_cache = {
            "variables": {},
            "functions": {}
        }

    def datacollector ( self, node ) :
        if isinstance(node, slimit.ast.FuncDecl) :
            print(f"Found function {node.identifier.to_ecma()}")
            self.volatile_cache["functions"][node.identifier] = node
            return
        if isinstance(node, slimit.ast.VarDecl) :
            print(f"Found variable {node.identifier.to_ecma()}")
            self.volatile_cache["variables"][node.identifier] = node
            return
        print(f"Datacollect: {node.__class__.__name__}")

    def constantpropagator ( self, node ) :
        if isinstance(node, slimit.ast.FunctionCall) :
            print(f"FunctionCall {node.__dict__}")
            return
        print(f"Constantprop: {node.__class__.__name__}")

    def parse ( self, code ) :
        print("parse")
        parser = SlimitParser()
        program = parser.parse(code)
        self.visit(program, self.datacollector)
        self.visit(program, self.constantpropagator)
        self.uldl = program.to_ecma()

    def visit ( self, node, visitor ) :
        visitor(node)
        if isinstance(node, slimit.ast.Program) :
            for child in node._children_list :
                self.visit(child, visitor)
            return
        if isinstance(node, slimit.ast.FuncDecl) :
            return
        if isinstance(node, slimit.ast.ExprStatement) :
            self.visit(node.expr, visitor)
            return
        if isinstance(node, slimit.ast.FunctionCall) :
            return
        if isinstance(node, slimit.ast.VarStatement) :
            for child in node._children_list :
                self.visit(child, visitor)
            return
        if isinstance(node, slimit.ast.VarDecl) :
            return

        print(node.__dict__)
        print(node.to_ecma())
        raise Exception("Unhandled node: " + node.__class__.__name__)

    def parse_file ( self, filename ) :
        if not os.path.isfile(filename) :
            print("File not found: " + filename)
            return
        with open( filename, "r" ) as f :
            code = f.read()
        self.parse(code)
    def save_file ( self, filename ) :
        with open( filename, "w" ) as f :
            f.write(self.uldl)
