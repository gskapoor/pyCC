from enum import Enum, auto
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


class ExpressionNode(ASTNode):
    def assemble(self):
        raise ValueError(
            "ExpressionNode is an Abstract Class, something went terribly wrong"
        )


class ConstIntNode(ExpressionNode):
    def __init__(self, value: int):
        self.value = value

    def __repr__(self):
        return f"ConstNode({repr(self.value)}"

    def assemble(self):
        return ImmediateASM(self.value)


class UnaryOperatorNode(Enum):
    NEG = auto()
    BITFLIP = auto()


class UnaryExpressionNode(ExpressionNode):
    def __init__(self, op: UnaryOperatorNode, expr: ExpressionNode):
        self.op = op
        self.expr = expr

    def __repr__(self):
        return f"Unary({repr(self.op)}, {repr(self.expr)})"


class ReturnNode(ASTNode):
    def __init__(self, expression: ExpressionNode):
        self.expression = expression

    def __repr__(self):
        return f"ReturnNode({repr(self.expression)})"

    def assemble(self):
        expr_asm = self.expression.assemble()
        return [MoveASM(expr_asm, RegisterASM(RegisterEnum.EAX)), ReturnASM()]


class FunctionNode(ASTNode):
    def __init__(self, identifier: IdentifierNode, statement: ReturnNode):
        self.identifier = identifier
        self.statement = statement

    def __repr__(self):
        return f"FunctionNode({repr(self.identifier)}, {repr(self.statement)})"

    def assemble(self):
        func_name = repr(self.identifier)
        statement_asm = self.statement.assemble()
        return FunctionASM(func_name, statement_asm)


class ProgramNode(ASTNode):
    def __init__(self, function: FunctionNode):
        self.function = function

    def __repr__(self):
        return f"ProgramNode({repr(self.function)})"

    def assemble(self):
        func_asm = self.function.assemble()
        return ProgramASM(func_asm)
