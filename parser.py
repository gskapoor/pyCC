

class ASTNode:
    # Base Node Class
    pass

class ProgramNode(ASTNode):
    def __init__(self, function):
        self.function = function

    def __repr__(self):
        return (f"ProgramNode({repr(self.functionDef)})")

class FunctionNode(ASTNode):
    def __init__(self, identifier, statement):
        self.identifier = identifier
        self.statement = statement

    def __repr__(self):
        return (f"FunctionNode({repr(self.identifier), repr(self.statement)})")

class ReturnNode(ASTNode):
    def __init__(self, expression):
        self.expression = expresion

    def __repr__(self):
        return (f"ReturnNode({repr(self.expression)})")

class Expression(ASTNode):
    def __init__(self, constant):
        self.constant = constant

    def __repr__(self):
        return (f"ReturnNode({repr(self.constant)})")

class Constant(ASTNode):
    def __init__(self, value):
        self.value = value

    def __repr__(self):
        return repr(self.value)

def parse(input):
    return Constant(1)
