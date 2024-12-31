from .ASTNode import (
    ASTNode,
    BinaryExpressionNode,
    BinaryOperatorNode,
    ConstIntNode,
    ExpressionNode,
    FunctionNode,
    IdentifierNode,
    UnaryExpressionNode,
    ReturnNode,
    ProgramNode,
    UnaryOperatorNode,
)
from .tackyNode import (
    BinaryOpTacky,
    BinaryTacky,
    ConstIntTacky,
    CopyTacky,
    FuncTacky,
    JumpIfNotZero,
    JumpIfZero,
    JumpTacky,
    Label,
    ProgramTacky,
    ReturnTacky,
    UnaryOpTacky,
    UnaryTacky,
    VarTacky,
)


OP_TABLE = {
    UnaryOperatorNode.NEG: UnaryOpTacky.NEG,
    UnaryOperatorNode.BITFLIP: UnaryOpTacky.BITFLIP,
    BinaryOperatorNode.ADD: BinaryOpTacky.ADD,
    BinaryOperatorNode.SUB: BinaryOpTacky.SUB,
    BinaryOperatorNode.MUL: BinaryOpTacky.MUL,
    BinaryOperatorNode.DIV: BinaryOpTacky.DIV,
    BinaryOperatorNode.MOD: BinaryOpTacky.MOD,
    BinaryOperatorNode.LSHIFT: BinaryOpTacky.LSHIFT,
    BinaryOperatorNode.RSHIFT: BinaryOpTacky.RSHIFT,
    BinaryOperatorNode.BITAND: BinaryOpTacky.BAND,
    BinaryOperatorNode.BITOR: BinaryOpTacky.BOR,
    BinaryOperatorNode.BITXOR: BinaryOpTacky.BXOR,
    BinaryOperatorNode.GE: BinaryOpTacky.GE,
    BinaryOperatorNode.GEQ: BinaryOpTacky.GEQ,
    BinaryOperatorNode.LE: BinaryOpTacky.LE,
    BinaryOperatorNode.LEQ: BinaryOpTacky.LEQ,
    BinaryOperatorNode.EQ: BinaryOpTacky.EQ,
    BinaryOperatorNode.NEQ: BinaryOpTacky.NEQ,
    BinaryOperatorNode.LAND: BinaryOpTacky.LAND,
    BinaryOperatorNode.LOR: BinaryOpTacky.LOR,
}


class TackyGen:
    def __init__(self):
        self.vars_used = 0
        self.labels_used = 0

    def genVariable(self):
        res = VarTacky(f".tmp{self.vars_used}")
        self.vars_used += 1
        return res

    def emit_tacky(self, node: ExpressionNode):
        match node:
            case ConstIntNode(value=val):
                return ConstIntTacky(val), []
            case UnaryExpressionNode(op=op, expr=expr):
                src, instructions = self.emit_tacky(expr)
                new_var = self.genVariable()
                instructions.append(UnaryTacky(OP_TABLE[op], src, new_var))
                return new_var, instructions
            case BinaryExpressionNode(
                op=BinaryOperatorNode.LOR, left_expr=left_expr, right_expr=right_expr
            ):
                new_var = self.genVariable()

                left_src, instructions = self.emit_tacky(left_expr)
                instructions.append(JumpIfNotZero(left_src, Label(f"or_true({self.labels_used})")))

                right_src, right_instructions = self.emit_tacky(right_expr)
                instructions += right_instructions
                instructions.append(JumpIfNotZero(right_src, Label(f"or_true({self.labels_used})")))
                instructions.append(CopyTacky(ConstIntTacky(0), new_var))
                instructions.append(JumpTacky(Label(f"or_end({self.labels_used})")))

                instructions.append(Label(f"or_true({self.labels_used})"))
                instructions.append(CopyTacky(ConstIntTacky(1), new_var))
                instructions.append(Label(f"or_end({self.labels_used})"))

                self.labels_used += 1
                return new_var, instructions
            case BinaryExpressionNode(
                op=BinaryOperatorNode.LAND, left_expr=left_expr, right_expr=right_expr
            ):
                new_var = self.genVariable()

                left_src, instructions = self.emit_tacky(left_expr)
                instructions.append(JumpIfZero(left_src, Label(f"and_false({self.labels_used})")))

                right_src, right_instructions = self.emit_tacky(right_expr)
                instructions += right_instructions
                instructions.append(JumpIfZero(right_src, Label(f"and_false({self.labels_used})")))
                instructions.append(CopyTacky(ConstIntTacky(1), new_var))
                instructions.append(JumpTacky(Label(f"and_end({self.labels_used})")))

                instructions.append(Label(f"and_false({self.labels_used})"))
                instructions.append(CopyTacky(ConstIntTacky(0), new_var))
                instructions.append(Label(f"and_end({self.labels_used})"))

                self.labels_used += 1
                return new_var, instructions
            case BinaryExpressionNode(
                op=op, left_expr=left_expr, right_expr=right_expr
            ):
                left_src, left_instructions = self.emit_tacky(left_expr)
                right_src, right_instructions = self.emit_tacky(right_expr)
                instructions = left_instructions + right_instructions
                new_op = OP_TABLE[op]
                new_var = self.genVariable()
                instructions.append(BinaryTacky(new_op, left_src, right_src, new_var))
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
