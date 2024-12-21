from pyCC.pyCmp.ASTNode import (
    ASTNode,
    ConstIntNode,
    ExpressionNode,
    FunctionNode,
    IdentifierNode,
    UnaryExpressionNode,
    ReturnNode,
    ProgramNode,
    UnaryOperatorNode
)
from pyCC.pyCmp.tackyNode import ConstIntTacky, FuncTacky, ProgramTacky, ReturnTacky, UnaryOpTacky, UnaryTacky, VarTacky


OP_TABLE = {
    UnaryOperatorNode.NEG: UnaryOpTacky.NEG,
    UnaryOperatorNode.BITFLIP: UnaryOpTacky.BITFLIP,
}

class TackyGen:
    def __init__(self):
        self.vars_used = 0

    def genVariable(self):
        res = VarTacky(f".tmp{self.vars_used}")
        self.vars_used += 1
        return res

    def emit_tacky(self, node: ExpressionNode):
        match node:
            case ConstIntNode(value=val):
                return ConstIntTacky(val), []
            case UnaryExpressionNode(op=op, expr=expr):
                src,instructions = self.emit_tacky(expr)
                new_var = self.genVariable()
                instructions.append(UnaryTacky(OP_TABLE[op], src, new_var))
                return new_var, instructions


        raise TypeError("Attempted to run 'emit_tacky' on a non-expression")

    def create(self, node: ASTNode):
        ## This should only be run at non instruction-producing Nodes
        match node:
            case ProgramNode(function=func):
                res = self.create(func)
                return ProgramTacky(res)
            case FunctionNode(identifier=name, statement=statement):
                return FuncTacky(self.create(name), self.create(statement))
            case ReturnNode(expression=expression):
                src, instructions = self.emit_tacky(expression)
                instructions.append(ReturnTacky(src))
                return instructions
            case IdentifierNode(name=name):
                return name
            case _:
                raise ValueError("Error generating Tacky")


def tackify(ast_program: ProgramNode):
    tacky_generator = TackyGen()
    res = tacky_generator.create(ast_program)
    return res
