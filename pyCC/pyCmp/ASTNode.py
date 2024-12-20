from .ASMNode import (
    FunctionASM,
    ImmediateASM,
    MoveASM,
    ProgramASM,
    RegisterASM,
    RegisterEnum,
    ReturnASM,
)


class ASTNode:
    # Base Node Class
    pass


class IdentifierNode(ASTNode):
    def __init__(self, name: str):
        self.name = name

    def __repr__(self):
        return self.name


class ConstantNode(ASTNode):
    def __init__(self, value):
        self.value = value

    def __repr__(self):
        return repr(self.value)

    def assemble(self):
        return ImmediateASM(self.value)


class ExpressionNode(ASTNode):
    def __init__(self, constant: ConstantNode):
        # This should be refactored to have the bottom (constant) inherit
        self.constant = constant

    def __repr__(self):
        return f"ExprNode({repr(self.constant)})"

    def assemble(self):
        return self.constant.assemble()


class ReturnNode(ASTNode):
    def __init__(self, expression: ExpressionNode):
        self.expression = expression

    def __repr__(self):
        return f"ReturnNode({repr(self.expression)})"

    def assemble(self):
        exprASM = self.expression.assemble()
        return [MoveASM(exprASM, RegisterASM(RegisterEnum.EAX)), ReturnASM()]


class FunctionNode(ASTNode):
    def __init__(self, identifier: IdentifierNode, statement: ReturnNode):
        self.identifier = identifier
        self.statement = statement

    def __repr__(self):
        return f"FunctionNode({repr(self.identifier)}, {repr(self.statement)})"

    def assemble(self):
        funcName = repr(self.identifier)
        statementAsm = self.statement.assemble()
        return FunctionASM(funcName, statementAsm)


class ProgramNode(ASTNode):
    def __init__(self, function: FunctionNode):
        self.function = function

    def __repr__(self):
        return f"ProgramNode({repr(self.function)})"

    def assemble(self):
        funcASM = self.function.assemble()
        return ProgramASM(funcASM)
