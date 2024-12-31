from enum import Enum, auto
from typing import List


class TackyNode:
    # abstract class
    # Maybe i add stuff here to give errors?
    pass


class UnaryOpTacky(Enum):
    NEG = auto()
    BITFLIP = auto()
    NOT = auto()


class BinaryOpTacky(Enum):
    ADD = auto()
    SUB = auto()
    MUL = auto()
    DIV = auto()
    MOD = auto()
    LSHIFT = auto()
    RSHIFT = auto()
    BAND = auto()
    BOR = auto()
    BXOR = auto()
    GE = auto()
    GEQ = auto()
    LE = auto()
    LEQ = auto()
    EQ = auto()
    NEQ = auto()
    LAND = auto()
    LOR = auto()


class ValTacky(TackyNode):
    pass


class ConstIntTacky(ValTacky):
    def __init__(self, val: int):
        self.val = val

    def __repr__(self):
        return f"ConstInt({self.val})"


class VarTacky(ValTacky):
    def __init__(self, name: str):
        self.name = name

    def __repr__(self):
        return f"Var({self.name})"


class InstructionTacky(TackyNode):
    pass


class ReturnTacky(InstructionTacky):
    def __init__(self, val: ValTacky):
        self.val = val

    def __repr__(self):
        return f"Return({repr(self.val)})"


class UnaryTacky(InstructionTacky):
    def __init__(self, op: UnaryOpTacky, src: ValTacky, dst: VarTacky):
        self.op = op
        self.src = src
        self.dst = dst

    def __repr__(self):
        return f"Unary({self.op}, {repr(self.src)}, {repr(self.dst)})"


class BinaryTacky(InstructionTacky):
    def __init__(
        self, op: BinaryOpTacky, left_val: ValTacky, right_val: ValTacky, dst: VarTacky
    ):
        self.op = op
        self.left_val = left_val
        self.right_val = right_val
        self.dst = dst

    def __repr__(self):
        return f"Binary({self.op}, {repr(self.left_val)}, {repr(self.right_val)}, {repr(self.dst)})"


class CopyTacky(InstructionTacky):
    def __init__(self, src: ValTacky, dst: ValTacky):
        self.src = src
        self.dst = dst

    def __repr__(self):
        raise NotImplementedError()
    

class Jump(InstructionTacky):
    def __init__(self, target: str):
        self.target = target

    def __repr__(self):
        raise NotImplementedError()

class JumpIfZero(InstructionTacky):
    def __init__(self, condition: ValTacky, target: str):
        self.target = target

    def __repr__(self):
        raise NotImplementedError()

class JumpIfNotZero(InstructionTacky):
    def __init__(self, condition: ValTacky, target: str):
        self.target = target

    def __repr__(self):
        raise NotImplementedError()


class Label(InstructionTacky):
    def __init__(self, name: str):
        self.name = name

    def __repr__(self):
        raise NotImplementedError()


class FuncTacky(TackyNode):
    def __init__(self, identifier: str, instructions: List[InstructionTacky]):
        self.identifier = identifier
        self.instructions = instructions

    def __repr__(self):
        res = f"Func({self.identifier},["
        for instruction in self.instructions:
            res += repr(instruction)
            res += ", "
        res += "])"
        return res


class ProgramTacky(TackyNode):
    def __init__(self, func: FuncTacky):
        self.func = func

    def __repr__(self):
        return f"Prog({repr(self.func)})"
