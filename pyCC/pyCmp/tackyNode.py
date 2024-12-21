from enum import Enum, auto
from typing import List


class TackyNode:
    # abstract class
    # Maybe i add stuff here to give errors?
    pass


class UnaryOpTacky(Enum):
    NEG = auto()
    BITFLIP = auto()


class ValTacky(TackyNode):
    pass


class ConstIntTacky(ValTacky):
    def __init__(self, val: int):
        self.val = val


class VarTacky(ValTacky):
    def __init__(self, name: str):
        self.name = name


class InstructionTacky(TackyNode):
    pass


class ReturnTacky(InstructionTacky):
    def __init__(self, val: ValTacky):
        self.val = val


class UnaryTacky(InstructionTacky):
    def __init__(self, op: UnaryOpTacky, src: ValTacky, dst: VarTacky):
        self.op = op
        self.src = src
        self.dst = dst


class FuncTacky(TackyNode):
    def __init__(self, identifier: str, instructions: List[InstructionTacky]):
        self.identifier = identifier
        self.instructions = instructions


class ProgramTacky(TackyNode):
    def __init__(self, func: FuncTacky):
        self.func = func
